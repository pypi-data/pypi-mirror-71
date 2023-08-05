// Value formatting functions for dygraphs

var formatters = {

    percent: function(value) {
        // Formats a ratio as a percentage
        if (isNaN(value) || value == null) {
            return ''
        }
        value = value * 100;
        return (value > 0 && value < 10 ? value.toFixed(1) : Math.round(value)) + '%';
    },

    decimal: function(value) {
        // Formats to a number with 2 decimal places
        if (isNaN(value) || value == null) {
            return ''
        }
        return value.toFixed(2);
    },

    decimal_3: function(value) {
        // Formats to a number with 3 decimal places
        if (isNaN(value) || value == null) {
            return ''
        }
        return value.toFixed(3);
    },

    number: function(value) {
        // Formats a number intelligently. Returns an integer with thousands separators
        // for integers and large decimals; returns a decimal for small decimals
        if (isNaN(value) || value == null) {
            return ''
        }
        if (value >= 1000) {
            return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        if (value === parseInt(value)) {
            return value;
        }
        return value.toFixed(value < 10 ? 2 : 1);
    },

    capacity: function(value) {
        if (isNaN(value) || value == null) {
            return ''
        }
        var units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
        for (var i = 0; i < units.length; i++) {
            if (value < 1000) break;
            value /= 1000.0
        }
        return value.toFixed(1) + '&nbsp;<small>' + units[i] + '</small>';
    },

    blocksize: function(value) {
        value /= 1024.0;
        return value.toFixed(1) + '&nbsp;<small>KiB</small>'
    },

    throughput: function(value){
        if (isNaN(value) || value == null) {
            return ''
        }
         var units = ['B/s', 'KiB/s', 'MiB/s', 'GiB/s', 'TiB/s', 'PiB/s', 'EiB/s', 'ZiB/s', 'YiB/s']
         for (var i = 0; i < units.length; i++) {
            if (value < 1000) break;
            value /= 1000.0
         }
        return value.toFixed(1) + '&nbsp;<small>' + units[i] + '</small>';
    }

}
