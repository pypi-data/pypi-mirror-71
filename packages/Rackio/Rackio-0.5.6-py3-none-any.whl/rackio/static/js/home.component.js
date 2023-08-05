'use strict';

// Register `home` component, along with its associated controller and template
angular.
    module('home').
        component('home', {
            templateUrl: '/template/home.html',
            controller: function HomeController($scope, $http, $interval) {

                // Our labels and three data series
                $scope.data1 = {
                    series: [
                        [5, 4, 3, 7, 5, 10],
                    ]
                };

                $scope.data2 = {
                    series: [
                        [5, 4, 3, 7, 5, 10],
                    ]
                };

                $scope.data3 = {
                    series: [
                        [5, 4, 3, 7, 5, 10],
                    ]
                };

                $scope.data4 = {
                    series: [
                        [5, 4, 3, 7, 5, 10],
                    ]
                };
                
                // We are setting a few options for our chart and override the defaults
                this.options = {
                    // Don't draw the line chart points
                    showPoint: false,
                    // Disable line smoothing
                    lineSmooth: false,
                    // X-Axis specific configuration
                    axisX: {
                        // We can disable the grid for this axis
                        showGrid: true,
                        // and also don't show the label
                        showLabel: false,
                        divisor: 4,
                    },
                    // Y-Axis specific configuration
                    axisY: {
                        // Lets offset the chart a bit from the labels
                        offset: 60,
                        divisor: 4,
                        high: 9.8,
                        low: 8.75,
                        // The label interpolation function enables you to modify the values
                        // used for the labels on each axis. Here we are converting the
                        // values into million pound.
                        labelInterpolationFnc: function(value) {
                            return Math.round(value * 100) / 100 + ' psi';
                        }
                    }
                };
                
                // All you need to do is pass your configuration as third parameter to the chart function
                $scope.chart1 = new Chartist.Line('.ct-chart1', this.data1, this.options);

                // All you need to do is pass your configuration as third parameter to the chart function
                $scope.chart2 = new Chartist.Line('.ct-chart2', this.data2, this.options);

                // All you need to do is pass your configuration as third parameter to the chart function
                $scope.chart3 = new Chartist.Line('.ct-chart3', this.data3, this.options);

                $scope.chart4 = new Chartist.Line('.ct-chart4', this.data4, this.options);

                this.updateChart = function(){
                    
                    var stop = moment().subtract(2, 'seconds').format('YYYY-MM-DD HH:mm:ss');
                    var start = moment().subtract(30, 'seconds').format('YYYY-MM-DD HH:mm:ss');
                    
                    var params = {
                        tstart: start,
                        tstop: stop,
                        tags: ["original", "var", "dewhite"]
                    };

                    var url = '/api/trends', data = params, config='application/json';
                    $http.post(url, data, config).then(function (response) {

                        $scope.data1 = {
                            series: [
                                response.data[0].waveform.values,
                            ]
                        }

                        $scope.data2 = {
                            series: [
                                response.data[1].waveform.values,
                            ]
                        }

                        $scope.data4 = {
                            series: [
                                response.data[2].waveform.values,
                            ]
                        }

                    }, function (error) {

                        console.log(error);

                    });

                    params = {
                        tstart: start,
                        tstop: stop
                    };

                    var url = '/api/trends/filtered/var', data = params, config='application/json';
                    $http.post(url, data, config).then(function (response) {

                        console.log(response);

                        $scope.data3 = {
                            series: [
                                response.data.waveform.values,
                            ]
                        }

                        $scope.chart1.update($scope.data1, $scope.options);
                        $scope.chart2.update($scope.data2, $scope.options);
                        $scope.chart3.update($scope.data3, $scope.options);
                        $scope.chart4.update($scope.data4, $scope.options);

                    }, function (error) {

                        console.log(error);

                    });
                    
                };

                $interval(this.updateChart, 500);
            }
        }
);