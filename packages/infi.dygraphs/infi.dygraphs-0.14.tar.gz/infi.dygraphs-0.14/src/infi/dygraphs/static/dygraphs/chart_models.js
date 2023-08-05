
ChartData = Backbone.Model.extend({

    url: null,              // url to load the data from
    headers: {},            // headers to send when loading data
    chart_data: [],         // the currently loaded data points
    data_fields: null,      // array of field names in the data (loaded from the server)
    chart_start: null,      // first timestamp covered by the chart, in milliseconds
    chart_end: null,        // last timestamp covered by the chart, in milliseconds
    polling_interval: null, // frequency in which new data is added to the database, in seconds
    resampling_window: 0,   // size of time window in seconds for averaging the data points (0 - no averaging)
    loading: 0,             // a counter to know whether there's loading in progress
    req_counter: 0,         // ajax request counter used to ignore obsolete requests
    last_req_range: null,   // used to ignore duplicate requests

    initialize: function(attributes, options) {
        this.url = options.url;
        this.url_params = options.url_params || {};
        this.headers = options.headers || {};
        this.polling_interval = options.polling_interval || 300;
        this.throttledLoadNewData = _.throttle(_.bind(this.loadNewData, this), 2500);
        if (options.chart_start && options.chart_end) {
            this.chart_start = options.chart_start;
            this.chart_end = options.chart_end;
            this.loadAllData(options.chart_start, options.chart_end, true);
        }
    },

    setURL: function(url) {
        if (this.url != url) {
            this.url = url;
            this.loadAllData(this.chart_start, this.chart_end, true);
        }
    },

    setURLParams: function(params) {
        if (this.params != params) {
            this.url_params = params;
            this.loadAllData(this.chart_start, this.chart_end, true);
        }
    },

    getPollingInterval: function() {
        return this.polling_interval;
    },

    getChartStart: function() {
        return this.chart_start;
    },

    setChartStart: function(d) {
        if (d && this.chart_start != d.getTime()) {
            this.chart_start = d.getTime();
            this.trigger('change', [this.chart_start, this.chart_end]);
        }
    },

    getChartEnd: function() {
        return this.chart_end;
    },

    setChartEnd: function(d) {
        if (d && this.chart_end != d.getTime()) {
            this.chart_end = d.getTime();
            this.trigger('change', [this.chart_start, this.chart_end]);
        }
    },

    adjustChartStart: function() {
        // Set chart_start to the first available data point
        this.setChartStart(this.getFirstEntryDate());
    },

    adjustChartEnd: function() {
        // Set chart_end to the last available data point
        this.setChartEnd(this.getLastEntryDate());
    },

    getFirstEntryDate: function() {
        return this.chart_data.length ? _.first(this.chart_data)[0] : null;
    },

    getLastEntryDate: function() {
        return this.chart_data.length ? _.last(this.chart_data)[0] : null;
    },

    convertTimestamps: function(data) {
        // Convert timestamps to Date instances in each data point
        _.each(data, function(entry) {
            entry[0] = moment.utc(entry[0]).toDate();
        });
    },

    getChartData: function() {
        return this.chart_data;
    },

    setChartData: function(data) {
        // Replace all of the data points with the given ones
        this.convertTimestamps(data);
        this.chart_data = data;
        this.trigger('change', [this.chart_start, this.chart_end]);
    },

    addChartData: function(data) {
        // Append the given data points to chart_data
        if (data.length > 0) {
            if (data.length > 1500) {
                // Loaded too much, we can't possibly need so many points
                data.splice(1500);
            }
            this.convertTimestamps(data);
            this.chart_data = this.chart_data.concat(data);
            this.trigger('change', [this.chart_start, this.chart_end]);
        }
    },

    steps: [10, 30, 60, 120, 180, 240, 300, 600],

    calcResamplingWindow: function(chart_start, chart_end) {
        var range_in_hours = (chart_end - chart_start) / 3600 / 1000;
        if (range_in_hours <= 4) return 0;
        // Calculate the width of the resampling window in seconds
        var w = 10 * range_in_hours / 3;
        // Convert it to an int between 0 and 7
        var magnitude = Math.min(7, Math.round(Math.log(w)) - 3);
        // Round it to a "nice" number
        var step = this.steps[magnitude];
        return Math.round(w / step) * step;
    },

    loadAllData: function(chart_start, chart_end, force) {
        // Set the chart range and load all data within this range.
        // chart_start and chart_end are in milliseconds, or Moment instances.
        // force ensures that data is reloaded when it's true.
        if (!force) {
            // Do not load if it's the same date range
            if (chart_start == this.chart_start && chart_end == this.chart_end) return;
            // Do not load if there's an ongoing request for the same date range
            if (this.last_req_range && chart_start == this.last_req_range[0] && chart_end == this.last_req_range[1]) return;
        }
        this.last_req_range = [chart_start, chart_end];
        this.setLoading(true);
        this.trigger('changing', [chart_start, chart_end]);
        var resampling_window = this.calcResamplingWindow(chart_start, chart_end);
        // number of extra milliseconds to retrieve (prevents the data from ending before the chart's edge)
        var extra = Math.max(resampling_window, this.polling_interval) * 1000;
        var self = this;
        self.req_counter++;
        $.ajax({
            url: self.url,
            headers: self.headers,
            cache: false,
            context: self.req_counter, // becomes 'this' in the done callback
            data: _.extend({
                from: chart_start - extra,
                to: chart_end + extra,
                resample: resampling_window
            }, self.url_params)
        }).done(function(response) {
            if (this == self.req_counter) {
                self.chart_start = chart_start;
                self.chart_end = chart_end;
                self.resampling_window = resampling_window;
                self.data_fields = response.fields;
                self.setChartData(response.data);
            }
        }).fail(function(jqXHR, textStatus, errorThrown) {
            window.console && console.log(textStatus, errorThrown);
            self.trigger('loading:failed');
        }).always(function() {
            self.setLoading(false);
            self.last_req_range = null;
        });
    },

    loadNewData: function(to) {
        // Load any new data points that may have been created
        if (this.loading) return;
        var from = this.chart_start;
        if (this.chart_data.length > 0) {
            // Load only data after the latest timestamp that we currently have
            from = this.getLastEntryDate().getTime();
            // Check that at least resampling_window seconds have passed (we want only one data point per window)
            var elapsed = (new Date().getTime() - from) / 1000;
            if (elapsed < Math.max(this.resampling_window, this.polling_interval)) return;
        }
        this.setLoading(true);
        // number of extra milliseconds to retrieve (prevents the data from ending before the chart's edge)
        var extra = Math.max(this.resampling_window, this.polling_interval) * 1000;
        var self = this;
        self.req_counter++;
        $.ajax({
            url: self.url,
            headers: self.headers,
            cache: false,
            context: self.req_counter, // becomes 'this' in the done callback
            data: _.extend({
                from: from,
                to: to + extra,
                resample: self.resampling_window,
            }, self.url_params)
        }).done(function(response, status, xhr) {
            if (this == self.req_counter) {
                self.data_fields = response.fields;
                self.addChartData(response.data);
            }
        }).always(function() {
            self.setLoading(false);
        });
    },

    setLoading: function(loading) {
        if (loading) {
            this.loading++;
            if (this.loading == 1) {
                this.trigger('loading:started');
            }
        }
        else {
            this.loading--;
            if (this.loading == 0) {
                this.trigger('loading:ended');
            }
            else if (this.loading < 0) { // not supposed to happen
                this.loading = 0;
            }
        }
    },

    isLoading: function() {
        return (this.loading > 0);
    }

});


ChartDataWrapper = Backbone.Model.extend({

    // A base class for wrapping a ChatData instance (passed in the options as "parent")
    // and changing its behavior using the Decorator design pattern.

    getChartStart: function() {
        return this.parent.getChartStart();
    },

    getChartEnd: function() {
        return this.parent.getChartEnd();
    },

    getLastEntryDate: function() {
        return this.parent.getLastEntryDate();
    },

    getPollingInterval: function() {
        return this.parent.polling_interval;
    },

    loadAllData: function(chart_start, chart_end, force) {
        this.parent.loadAllData(chart_start, chart_end, force);
    },

    isLoading: function() {
        return this.parent.isLoading();
    }

});


PartialChartData = ChartDataWrapper.extend({

    // Wraps a ChartData model and extracts only specific columns from it.
    // This is used for displaying several charts derived from the same ChartData model.
    // The options passed to the constructor are expected to contain the parent model,
    // and either a column_indices array or a column_names array.

    initialize: function(attributes, options) {
        this.parent = options.parent;
        this.column_indices = options.column_indices || [];
        this.column_names = options.column_names;
        var self = this;
        _.each(['change', 'loading:started', 'loading:ended'], function(event) {
            self.listenTo(self.parent, event, function() {
                self.trigger(event);
            })
        });
    },

    getColumnNames: function() {
        return this.column_names.slice(0);
    },

    setColumnNames: function(column_names) {
        // Modify the column names that were passed in the original options
        this.column_indices = [];
        this.column_names = column_names;
    },

    getChartData: function() {
        // Get the chart data from the parent model, and convert each row
        var chart_data = this.parent.getChartData();
        if (!this.column_indices.length) {
            this.calcColumnIndices();
        }
        return _.map(chart_data, _.bind(this.extract, this));
    },

    extract: function(orig_row) {
        // Extract the wanted columns from a single row
        var row = [];
        for (j = 0; j < this.column_indices.length; j++) {
            row.push(orig_row[this.column_indices[j]]);
        }
        return row;
    },

    calcColumnIndices: function() {
        // Calculate the column_indices array from the column_names array
        var data_fields = this.parent.data_fields;
        if (data_fields) {
            this.column_indices = _.map(this.column_names, function(name) {
                var index = data_fields.indexOf(name);
                return index;
            });
            if (this.column_indices.indexOf(-1) != -1) {
                alert('ERROR: Some column names cannot be found in the chart data');
            }
        }
    }

});


ChartLabels = Backbone.Collection.extend({

    model: Backbone.Model,

    initialize: function(models, options) {
        this.available_colors = options.colors.slice(0);
    },

    addLabel: function(label, visible, css_class) {
        this.add([{
            id: this.id_for_label(label),
            label: label,
            visible: visible == null ? true : visible,
            css_class: css_class == null ? null : css_class,
            color: this.available_colors.shift()
        }]);
    },

    removeLabel: function(label) {
        var model = this.remove(this.id_for_label(label));
        if (model) {
            // Return the model's color back to the pool
            this.available_colors.unshift(model.get('color'));
        }
    },

    id_for_label: function(label) {
        return label.replace(/\W/g, '_');
    },

    setVisibility: function(index, visible) {
        this.at(index).set('visible', visible);
    }

});



MultiPartialChartData = ChartDataWrapper.extend({

    // Same as PartialChartData but with a support for multiple parents.
    // Expected options to be passed to the constructor: parent as list of models, column_indices as a list of lists
    // of columns to extract per each parent model
    // IMPORTANT: timestamp is assumed to be in index 0, no need to provide it in the list of column indices.

    initialize: function(attributes, options) {
        this.parent = options.parent;
        this.column_indices = options.column_indices;
        var self = this;
        _.each(['change', 'loading:started', 'loading:ended'], function(event) {
            _.each(self.parent, function(parent) {
                self.listenTo(parent, event, function() {
                    self.trigger(event);
                });
            });
        });
    },

    getChartData: function() {
        var partial_data = [];
        var partial_data_dict = {};
        var indices_count = _.reduce(this.column_indices, function(memo, indices){return memo + indices.length}, 0);
        for (var i = 0; i< this.parent.length; i++) {
            var column_indices = this.column_indices[i];
            var offset = _.reduce(this.column_indices.slice(0, i),
                function(memo, indices){return memo + indices.length}, 0);
            _.each(this.parent[i].getChartData(), function(chart_entry) {
                var timestamp = _.first(chart_entry);
                if (!_.has(partial_data_dict, timestamp)) {
                    var row = new Array(indices_count+1);
                    row.fill(null);
                    row[0] = timestamp;
                    partial_data_dict[timestamp] = row;
                }
                _.each(column_indices, function(column_index_val, column_index){
                    partial_data_dict[timestamp][offset + column_index + 1] = chart_entry[column_index_val];
                });
            });
        }
        _.each(_.keys(partial_data_dict).sort(function(a,b){return new Date(a) - new Date(b)}), function(key){
            partial_data.push(partial_data_dict[key])
        });
        return partial_data;
        },

    getChartStart: function() {
        return _.max(_.invoke(this.parent, 'getChartStart'));
    },

    getChartEnd: function() {
        return _.min(_.invoke(this.parent, 'getChartEnd'));
    },

    getLastEntryDate: function() {
        return _.min(_.invoke(this.parent, 'getLastEntryDate'));
    },

    getPollingInterval: function() {
        return _.max(_.pluck(this.parent, "polling_interval"));
    },

    loadAllData: function(chart_start, chart_end, force) {
        _.each(this.parent, function(parent){
            parent.loadAllData(chart_start, chart_end, force);
        });
    },

    isLoading: function() {
        return _.any(this.parent, function(parent){
                                    return parent.isLoading()
                                  }
                  );

    }

    });


