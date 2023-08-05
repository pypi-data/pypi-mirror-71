function get_template(selector) {
    // Returns an underscore template object for a template string that appears in the DOM
    return _.template($(selector).html().trim());
}

SyncedChartsView = Marionette.View.extend({

    // A layout containing one or more charts, stacked vertically.
    // The charts are kept in sync so that panning or zooming one of them
    // affects all the rest as well.

    template: _.noop,
    className: 'synced-charts-wrapper',
    charts: [],
    range: null,
    adjusting: false,
    highlighting: false,

    addChart: function(chart) {
        this.charts.push(chart);
        var name = 'slot_' + ($('.chart-slot', this.el).length + 1);
        var div = $('<div/>').addClass('chart-slot').addClass(name);
        this.$el.append(div);
        this.addRegion(name, '.' + name).show(chart);
    },

    getCharts: function() {
        return this.charts.slice(0);
    },

    syncCharts: function() {
        // Whenever the range of one chart changes, update the rest to match
        var self = this;
        _.each(self.getRegions(), function(region) {
            var view = region.currentView;
            if (view) {
                self.listenTo(view, 'redraw', self.adjustCharts);
                self.listenTo(view, 'highlight', self.highlight);
                self.listenTo(view, 'unhighlight', self.unhighlight);
            }
        });
    },

    setAdjusting: function(flag) {
        this.adjusting = flag;
    },

    adjustCharts: function(view) {
        // Change the range of all charts to match the range in the given view
        var self = this;
        if (!self.adjusting) {
            self.setAdjusting(true);
            self.range = view.chart.xAxisRange();
            _.each(self.getRegions(), function(region) {
                if (region.currentView && region.currentView != view && region.currentView.chart.xAxisRange() != self.range) {
                    try {
                        region.currentView.chart.updateOptions({dateWindow: self.range});
                    }
                    catch (e) {
                    }
                }
            });
            self.trigger('adjusted', self, view);
            self.setAdjusting(false);
        }
    },

    highlight: function(view, x, row, seriesName) {
        if (!this.highlighting) {
            this.highlighting = true;
            var self = this;
            _.each(this.getRegions(), function(region) {
                if (region.currentView && region.currentView != view) {
                    var chart = region.currentView.chart;
                    chart.setSelection(row, seriesName);
                    region.currentView.highlightCallback(null, x, chart.selPoints_, row, seriesName);
                }
            });
            this.highlighting = false;
        }
    },

    unhighlight: function(view) {
        if (!this.highlighting) {
            this.highlighting = true;
            var self = this;
            _.each(this.getRegions(), function(region) {
                if (region.currentView && region.currentView != view) {
                    //region.currentView.chart.setSelection(false);
                    region.currentView.unhighlightCallback();
                }
            });
            this.highlighting = false;
        }
    },

    resetZoom: function() {
        this.slot_1.currentView.resetZoom();
    },

    setRange: function(from_date, to_date) {
        this.setAdjusting(true);
        _.each(this.getRegions(), function(region) {
            region.currentView.setRange(from_date, to_date);
        });
        this.setAdjusting(false);
    },

    getRange: function() {
        // Get the current x-axis range of the charts
        return this.range;
    },

    goToDate: function(date, centered) {
        this.setAdjusting(true);
        var w = (this.range[1] - this.range[0]);
        var dateWindow = [date.valueOf() - w, date.valueOf()];
        if (centered) {
            dateWindow[0] += w / 2;
            dateWindow[1] += w / 2;
        }
        this.range = dateWindow;
        _.each(this.getRegions(), function(region) {
            region.currentView.chart.updateOptions({dateWindow: dateWindow});
        });
        this.setAdjusting(false);
    },

    toDataXCoord: function(x) {
        return this.slot_1.currentView.chart.toDataXCoord(x);
    },

    getSeries: function() {
        // Get the label of each series in the charts, and whether or not it is currently visible
        var series = [];
        var labels = this.slot_1.currentView.chart.getLabels();
        var visible = this.slot_1.currentView.chart.visibility();
        _.each(_.rest(labels), function(label, index) {
            var v = visible.length ? visible[index] : true;
            series.push({label: label, visible: v});
        });
        return series;
    },

    getChartType: function() {
        return this.slot_1.currentView.options.chart_type;
    },

    getAnnotations: function() {
        return this.slot_1.currentView.options.annotations.collection;
    },

    setAnnotationsVisibility: function(visible) {
        _.each(this.getRegions(), function(region) {
            if (region.currentView) {
                region.currentView.setAnnotationsVisibility(visible);
            }
        });
    },

    getAnnotationsVisibility: function() {
        return this.slot_1.currentView.annotations_visible;
    }

});


ChartView = Marionette.View.extend({

    template: _.noop,
    tagName: 'div',
    className: 'chart-wrapper',
    chart: null,
    spinner: null,
    legend: null,
    zoomed: false,
    unzoomed_range: null, // A pair of unix timestamps. Zooming out restores the chart to this range.
    annotations_visible: localStorage.getItem('annotations_visible') != 'false',
    chart_type_dynamic: false,
    storage_key: null,
    start_collapsed: false,
    highlighted_row: null,

    chartDefaults: {
        colors: ['#2ECC71', '#F64747', '#8E44AD', '#3498DB', '#E08283', '#67809F', '#DCC6E0', '#F89406', '#53dfc3', '#F4D03F', '#E4F1FE', '#A2DED0', '#AEA8D3', '#BDC3C7', '#C8F7C5', '#daebff', '#ECF0F1', '#19B5FE', '#D35400'],
        gridLineColor: '#3e3f45',
        axisLineColor: '#6c6f77',
        drawGapEdgePoints: true,
        axisLabelFontSize: 11,
        includeZero: true,
        showLabelsOnHighlight: false,
        labelsSeparateLines: true,
        labelsDivStyles: {background: 'rgba(255,255,255,0.7)'},
        pointSize: 3,
        highlightSeriesBackgroundAlpha: 1,
        valueRange: [0, null],
        hideOverlayOnMouseOut: false,
        errorBars: false,
        labelsUTC: true
    },

    chartTypes: {
        line: {
            stackedGraph: false,
            strokeWidth: 2,
            connectSeparatedPoints: false,
            colorSaturation: 0.6,
            fillAlpha: 0.3,
            fillGraph: false,
            highlightCircleSize: 8,
            highlightSeriesOpts: null
        },
        stacked: {
            stackedGraph: true,
            strokeWidth: 1,
            connectSeparatedPoints: false,
            colorSaturation: 1,
            fillAlpha: 0.3,
            fillGraph: true,
            highlightSeriesOpts: {
                highlightCircleSize: 8
            }
        }
    },

    initialize: function() {
        var self = this;
        // Re-render the chart when its data or annotation change
        self.listenTo(self.model, "change", self.refresh);
        if (self.options.annotations) {
            self.listenTo(self.options.annotations, "change", _.debounce(self.refresh, 10));
        }
        // Resize the chart when the window is resized (only width is flexible)
        $(window).resize(function() {
            self.resize();
        });
        // Load saved state for initial_visibility & start_collapsed
        var chart_options = self.options.chart_options;
        self.initial_visibility = chart_options.visibility;
        if (self.options.storage_key === undefined) {
            self.storage_key = btoa(chart_options.title + "_" + chart_options.labels);
        }
        else {
            self.storage_key = self.options.storage_key;
        }
        self.restoreState();
        // Build the chart_labels collection, used for rendering the legend
        var colors = chart_options.colors || self.chartDefaults.colors;
        self.chart_labels = new ChartLabels(null, {colors: colors});
        var labels = chart_options.labels || self.model.labels;
        _.each(_.rest(labels), function(label, index) {
            var visible = self.initial_visibility ? self.initial_visibility[index] : true;
            self.chart_labels.addLabel(label, visible);
        });
        // Match the visibility of the chart series to the chart labels
        chart_options.visibility = self.chart_labels.pluck('visible');
    },

    refresh: function() {
        if (this.chart) {
            this.chart.updateOptions({
                file: this.model.getChartData(),
                dateWindow: [this.model.getChartStart(), this.model.getChartEnd()]
            });
        }
        else {
            this.render();
        }
        // Remember the unzoomed range
        if (!this.zoomed) {
            this.unzoomed_range = this.chart.xAxisRange();
        }
        // Restore selected point if it exists, or show the rightmost values by default
        if (this.highlighted_row) {
            this.showValuesForRow(this.highlighted_row);
        }
        else {
            this.showLastValues();
        }
    },

    render: function() {
        var self = this;
        // Create the title and chart area (we render the title ourselves for better control over styling)
        self.$el.append(self.renderTitle());
        self.$el.append(self.renderLegend());
        self.$el.append('<div class="chart-padding"><div class="chart"></div></div>');
        // Instantiate the chart
        var dateWindow = [self.model.getChartStart() || Date.now() - $('#chart-range').val() * 3600 * 1000,
                          self.model.getChartEnd() || Date.now()];
        if (!self.options.chart_options.labelsKMG2 && !(self.options.chart_options.axes && self.options.chart_options.axes.y)) {
            // Add the default formatter since no other was specified
            self.options.chart_options.axes = {y: {valueFormatter: formatters.number, axisLabelFormatter: formatters.number}};
        }
        self.chart = new Dygraph(
            $('.chart', self.el)[0],
            self.model.getChartData(),
            _.extend({
                        dateWindow: dateWindow,
                        height: self.calcHeight(),
                        zoomProgressCallback: _.bind(self.zoomProgressCallback, self),
                        zoomCallback: _.bind(self.zoomCallback, self),
                        highlightCallback: _.bind(self.highlightCallback, self),
                        unhighlightCallback: _.bind(self.unhighlightCallback, self),
                        drawHighlightPointCallback: _.bind(self.drawHighlightPointCallback, self),
                        annotationClickHandler: _.bind(self.annotationClickHandler, self)
                     },
                     self.chartDefaults,
                     self.chartTypes[self.options.chart_type || 'line'],
                     self.options.chart_options,
                     {title: null})
        );
        // Show spinner when loading
        if (self.model.isLoading()) self.showSpinner();
        self.listenTo(self.model, "loading:started", self.showSpinner);
        self.listenTo(self.model, "loading:ended", self.hideSpinner);
        // Override the resetZoom function to zoom out to the user-specified range
        self.chart.resetZoom = _.bind(self.resetZoom, self);
        // Override the evaluateAnnotations function to allow annotations that don't match specific data points
        self.chart.layout_._evaluateAnnotations = _.bind(self.evaluateAnnotations, self);
        // Reload data when panning the chart
        var debouncedLoadData = _.debounce(_.bind(self.loadData, self), 250);
        self.chart.updateOptions({
            drawCallback: function(chart, initial) {
                self.resize();
                if (!initial) {
                    self.trigger('redraw', self);
                    debouncedLoadData();
                }
            }
        });
    },

    onShow: function() {
        // At this point the view has been added to its parent, so we can collapse it if necessary
        if (this.start_collapsed) {
            this.$el.parent().addClass('collapsed').height(38);
        }
    },

    renderTitle: function() {
        var h2 = $('<h2/>').text(this.options.chart_options.title);
        var toggler = $('<i/>').addClass('glyphicon glyphicon-circle-arrow-down toggler');
        h2.append(toggler);
        var self = this;
        toggler.on('click', function() {
            var target = self.$el.parent();
            target.toggleClass('collapsed');
            if (target.hasClass('collapsed')) {
                target.animate({height: h2.outerHeight()}, 300);
            }
            else {
                target.animate({height: self.$el.outerHeight()}, 300);
            }
            self.saveState();
        });
        if (this.options.help_text) {
            var a = $('<i/>').addClass('icon-help-circled').attr('title', this.options.help_text);
            h2.append(a);
            a.tooltip({
                position: {my: 'right', at: 'left-5'},
                tooltipClass: 'ui-tooltip-right-arrow'
            });
        }
        return h2;
    },

    renderLegend: function() {
        this.legend = new LegendView({labels: this.chart_labels});
        this.legend.on('visibility-changed', this.setVisibility, this);
        return this.legend.render();
    },

    resize: function() {
        this.chart.resize(this.calcWidth(), this.calcHeight());
    },

    calcHeight: function() {
        return Math.max(this.options.height || 165, 30 * this.chart_labels.length - 45);
    },

    calcWidth: function() {
        return this.$el.width() - this.legend.$el.width() - 40;
    },

    getVisibility: function(index) {
        return this.chart.visibility()[index];
    },

    setVisibility: function(index, visible) {
        this.chart.setVisibility(index, visible);
        this.chart_labels.setVisibility(index, visible);
        this.saveState();
    },

    setAnnotationsVisibility: function(visible) {
        if (visible != this.annotations_visible) {
            this.annotations_visible = visible;
            localStorage.setItem('annotations_visible', visible);
            this.refresh();
        }
    },

    evaluateAnnotations: function() {
        // This replaces the default DygraphLayout._evaluateAnnotations function in order to read the annotations
        // from our ChartAnnotations collection, and also to allow annotations that are not tied to an existing
        // point in the chart's data.
        if (this.options.annotations == undefined) return;
        var chart = this.chart;
        if (this.annotations_visible) {
            var canvasy = chart.toDomYCoord(0);
            var range = this.chart.xAxisRange();
            var items = this.options.annotations.get(range[0], range[1]);
            chart.layout_.annotated_points = _.map(items, function(item) {
                return {
                    xval: item.x,
                    yval: 0,
                    canvasx: chart.toDomXCoord(item.x),
                    canvasy: canvasy,
                    annotation: item
                };
            });
        }
        else {
            chart.layout_.annotated_points = [];
        }
    },

    setRange: function(from_date, to_date) {
        this.unzoomed_range = [from_date.valueOf(), to_date.valueOf()];
        this.resetZoom();
    },

    resetZoom: function() {
        // Reset the zoom level of the chart
        this.model.loadAllData(this.unzoomed_range[0], this.unzoomed_range[1]);
        this.zoomed = false;
    },

    zoomProgressCallback: function(zoomContext) {
        // Subclasses can override this to provide visual feedback while selecting a zoom range.
        // zoomContext is an object with these (and other) properties: isZooming, dragStartX, dragEndX
    },

    zoomCallback: function(minDate, maxDate, yRanges) {
        // Remember the unzoomed range
        if (!this.zoomed) {
            this.unzoomed_range = this.chart.xAxisRange();
        }
        // Enforce a minimum xaxis range by preventing excessive zooming
        var minimal_range = Math.max(this.model.getPollingInterval() * 2, 60) * 1000;
        var milliseconds = maxDate - minDate;
        if (milliseconds >= minimal_range) {
            this.model.loadAllData(minDate, maxDate);
            this.zoomed = true;
        }
    },

    showValues: function(x, points) {
        if (x < 0) {
            this.legend.clear();
            return;
        }
        //adjusting the given timestamp (in milliseconds) to the current timezone
        var adjusted_time = moment(x).tz(moment.defaultZone.name);
        var values = this.prepareValuesForDisplay(points);
        this.legend.show(adjusted_time, values);
    },

    prepareValuesForDisplay: function(points) {
        var self = this;
        var opts = self.chart.optionsViewForAxis_('y');
        var valueFormatter = opts('valueFormatter');
        var values = {};
        _.each(points, function(point) {
            var value = valueFormatter(point.yval, opts, point.name, self.chart);
            values[point.name] = value == 'NaN' ? '' : value;
        });
        return values;
    },

    showValuesForRow: function(row) {
        try {
            if (row && row >= 0) {
                this.chart.setSelection(row);
                this.showValues(this.chart.lastx_, this.chart.selPoints_);
                return;
            }
        }
        catch (e) {
        }
        this.legend.clear();
    },

    showLastValues: function() {
        var row = this.chart.findClosestRow($('canvas', this.el).width());
        this.showValuesForRow(row);
    },

    highlightCallback: function(event, x, points, row, seriesName) {
        this.highlighted_row = row;
        this.showValues(x, points);
        this.trigger('highlight', this, x, row, seriesName);
    },

    unhighlightCallback: function(event) {
        this.highlighted_row = null;
        this.showLastValues();
        this.trigger('unhighlight', this);
    },

    drawHighlightPointCallback: function(g, series, ctx, cx, cy, color, radius) {
        if (this.highlighted_row) {
            ctx.beginPath();
            ctx.arc(cx, cy, radius / 2, 0, 2 * Math.PI, false);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(255,255,255,0.4)';
            ctx.fill();
        }
    },

    annotationClickHandler: function(annotation, point, dygraph, event) {
        edit_annotation(annotation.id);
    },

    loadData: function() {
        var range = this.chart.xAxisRange();
        //this.model.loadDataIntelligently(range[0], range[1]);
        this.model.loadAllData(range[0], range[1]);
    },

    showSpinner: function() {
        if (!this.spinner) {
            var opts = _.extend(
                {
                    lines: 15, // The number of lines to draw
                    length: 0, // The length of each line
                    width: 3, // The line thickness
                    scale: 1,
                    radius: 20, // The radius of the inner circle
                    corners: 1, // Corner roundness (0..1)
                    rotate: 0, // The rotation offset
                    direction: 1, // 1: clockwise, -1: counterclockwise
                    color: '#bbb', // #rgb or #rrggbb or array of colors
                    fadeColor: 'transparent',
                    animation: 'spinner-line-fade-quick',
                    speed: 1, // Rounds per second
                    shadow: '0 0 1px transparent', // Whether to render a shadow
                    className: 'spinner', // The CSS class to assign to the spinner
                    zIndex: 100 // The z-index (one less than jquery ui dialog)
                },
                this.options.spinner_options
            );
            this.spinner = new Spinner(opts);
        }
        this.spinner.spin(this.$el.find('.chart').get(0));
    },

    hideSpinner: function() {
        if (this.spinner) {
            this.spinner.stop();
        }
    },

    isLoading: function() {
        return this.model.loading;
    },

    saveState: function() {
        // Save user choices in local storage
        if (this.storage_key) {
            var state = {
                visibility: this.chart.visibility(),
                collapsed: this.$el.parent().hasClass('collapsed')
            }
            localStorage.setItem(this.storage_key, JSON.stringify(state));
        }
    },

    restoreState: function() {
        // Restore user choices from local storage
        if (this.storage_key) {
            var serialized_state = localStorage.getItem(this.storage_key);
            if (serialized_state) {
                var state = JSON.parse(serialized_state);
                this.initial_visibility = state.visibility;
                this.start_collapsed = state.collapsed || false;
            }
        }
    },

    addSeries: function(label, css_class) {
        this.chart_labels.addLabel(label, true, css_class);
        this._updateChartSeries();
    },

    removeSeries: function(label) {
        this.chart_labels.removeLabel(label);
        this._updateChartSeries();
    },

    _updateChartSeries: function() {
        this.chart.updateOptions({
            labels: ['timestamp'].concat(this.chart_labels.pluck('label')),
            colors: this.chart_labels.pluck('color'),
            visibility: this.chart_labels.pluck('visible')
        }, true);
    }

});


// Add a zoomProgressCallback option
Dygraph.OPTIONS_REFERENCE['zoomProgressCallback'] = {};


// Override the default startZoom implementation to call the zoomProgressCallback
Dygraph.Interaction.startZoom = function(event, g, context) {
    Dygraph.Interaction.startZoom(event, g, context);
    g.getFunctionOption('zoomProgressCallback')(context);
};


// Override the default moveZoom implementation to prevent vertical zoom,
// and to call the zoomProgressCallback
Dygraph.moveZoom = function(event, g, context) {

    context.zoomMoved = true;
    context.dragEndX = Dygraph.dragGetX_(event, context);
    context.dragEndY = Dygraph.dragGetY_(event, context);

    context.dragDirection = Dygraph.HORIZONTAL; // Override: direction is always horizontal

    g.drawZoomRect_(
        context.dragDirection,
        context.dragStartX,
        context.dragEndX,
        context.dragEndY, // Override: dragEndY instead of dragStartY
        context.dragEndY,
        context.prevDragDirection,
        context.prevEndX,
        context.prevEndY
    );

    context.prevEndX = context.dragEndX;
    context.prevEndY = context.dragEndY;
    context.prevDragDirection = context.dragDirection;

    g.getFunctionOption('zoomProgressCallback')(context);

};


// Override the default endZoom implementation to call the zoomProgressCallback
Dygraph.endZoom = function(event, g, context) {
    Dygraph.Interaction.endZoom(event, g, context);
    g.getFunctionOption('zoomProgressCallback')(context);
};


// Override the default doZoomXDates_ implementation so that all it does
// is call the zoomCallback (without changing the chart's range). This way
// zoomCallback can ask the model to load the date range, and once loaded -
// the chart is redrawn with the new range.
Dygraph.prototype.doZoomXDates_ = function(minDate, maxDate) {
    this.getFunctionOption("zoomCallback").call(this, minDate, maxDate, this.yAxisRanges());
};

// Override the default startPan implementation to prevent vertical pan
var defaultStartPan = Dygraph.startPan;
Dygraph.startPan = function(event, g, context) {
    defaultStartPan(event, g, context);
    context.is2DPan = false;
};

// Prevent vertical pan and zoom on touchscreens
Dygraph.Interaction.defaultModel.touchstart = function(event, g, context) {
    Dygraph.Interaction.startTouch(event, g, context);
    context.touchDirections = {x: true, y: false};
};


// Override the default base-2 labels
Dygraph.KMG2_BIG_LABELS = [
    '&nbsp;<small>KiB</small>',
    '&nbsp;<small>MiB</small>',
    '&nbsp;<small>GiB</small>',
    '&nbsp;<small>TiB</small>',
    '&nbsp;<small>PiB</small>',
    '&nbsp;<small>EiB</small>',
    '&nbsp;<small>ZiB</small>',
    '&nbsp;<small>YiB</small>'
];


// In case the default timezone hasn't been set, autodetect it
if (!moment.defaultZone) {
    try {
        moment.tz.setDefault(moment.tz.guess());
    }
    catch {
        moment.tz.setDefault('UTC');
    }
}


// An adapter between Dygraph and Moment instances, to
// bridge between date fields that are defined in Dygraph
// and date fields that are used in moment.js
var MomentAdapter = {

    MOMENT_FIELDS: ['y', 'M', 'd', 'h', 'm', 's', 'ms'],

    createInTimezone: function(d) {
        return moment(d).tz(moment.defaultZone.name);
    },

    get: function(m, datefield) {
        var momentfield = this.MOMENT_FIELDS[datefield];
        return m.get(momentfield);
    },

    set: function(m, datefield, value) {
        var momentfield = this.MOMENT_FIELDS[datefield];
        return m.set(momentfield, value);
    },

    add: function(m, datefield, value) {
        if (!value) return m;
        var momentfield = this.MOMENT_FIELDS[datefield];
        return m.add(value, momentfield);
    },

    startOf: function(m, datefield) {
        var momentfield = this.MOMENT_FIELDS[datefield];
        return m.startOf(momentfield);
    }

}

// Overrides the default implementation because our getDateAxis
// uses Moment instances instead of regular Date objects
Dygraph.dateAxisLabelFormatter = function(date, granularity, opts) {
    // date should be a moment instance
    if (granularity >= Dygraph.DECADAL) {
        return date.format('YYYY');
    }
    else if (granularity >= Dygraph.MONTHLY) {
        return date.format('MMM&#160;YYYY');
    }
    else {
        var hms = date.format('HH:mm:ss');
        if (hms === '00:00:00' || granularity >= Dygraph.DAILY) {
            return date.format('DD&#160;MMM');
        }
        else if (granularity >= Dygraph.MINUTELY) {
            return hms.substring(0, 5);
        }
        else {
            return hms;
        }
    }
};


// Overrides the default implementation in order to display date ticks
// in Moment's default timezone (Dygraph only knows how to display
// the local timezone or UTC)
Dygraph.getDateAxis = function(start_time, end_time, granularity, opts, dg) {

    var formatter = Dygraph.dateAxisLabelFormatter;
    var datefield = Dygraph.TICK_PLACEMENT[granularity].datefield;
    var step = Dygraph.TICK_PLACEMENT[granularity].step;

    var start_date = MomentAdapter.createInTimezone(start_time);
    var end_date = MomentAdapter.createInTimezone(end_time);
    var tick_date = moment(start_date);

    // Choose a nice tick position before the initial instant.
    var start_date_offset = MomentAdapter.get(start_date, datefield) % step;
    if (granularity == Dygraph.WEEKLY) {
        // This will put the ticks on Sundays.
        start_date_offset = start_date.day();
    }
    MomentAdapter.add(tick_date, datefield, -start_date_offset);
    MomentAdapter.startOf(tick_date, datefield);

    // Generate the ticks
    var ticks = [];
    while (tick_date <= end_date) {
        MomentAdapter.add(tick_date, datefield, step);
        ticks.push({
            v: tick_date.valueOf(),
            label: formatter(tick_date, granularity, opts, dg)
        });
    }
    return ticks;
}

LegendView = Marionette.View.extend({

    tagName: 'div',
    className: 'legend',

    events: {
        'change': 'visibilityChanged'
    },

    initialize: function(options) {
        this.labels = options.labels;
        this.labels.on('all', _.debounce(_.bind(this.render, this), 100));
    },

    render: function() {
        var self = this;
        var template = get_template('#legend-template');
        var item_template = get_template('#legend-item-template');
        self.$el.empty().append(template({legend: self}));
        var items = self.$el.find('.legend-items');
        self.labels.each(function(model, index) {
            var data = {
                model:      model,
                index:      index,
                id:         _.uniqueId('legend-item-')
            }
            items.append(item_template(data));
        });
        return self.$el;
    },

    show: function(date, values) {
        // Expects the date to display, and an object mapping series labels to their values
        var self = this;
        var date_ = date.format('YYYY-MM-DD');
        var hour_ = date.format('HH:mm:ss');
        $('.legend-timestamp span', self.el).eq(0).text(date_);
        $('.legend-timestamp span', self.el).eq(1).text(hour_);
        _.each(values, function(value, label) {
            $('.' + self.labels.id_for_label(label) + ' .legend-value', self.el).html(value);
        });
    },

    clear: function() {
        $('.legend-timestamp span, .legend-value', this.el).html('');
    },

    visibilityChanged: function(event) {
        var target = $(event.target);
        target.closest('.legend-item').find('.legend-value').text('');
        this.trigger('visibility-changed', target.data('index'), target.prop('checked'));
    }

});
