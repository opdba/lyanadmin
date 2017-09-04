/**
 * Created by pazl on 2016/9/12.
 */

$(function () {
    $('#container').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 35,
                beta: 0
            }
        },
        colors:[
                '#D82D3E',
                '#64B5E4'
              ],
        title: {
            text: '磁盘空间'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: false,
                    format: '{point.name}',
                    //distance:0
                },
                showInLegend: true
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            type: 'pie',
            name: 'Browser share',
            data: [
                ['已用:55%',   55.0],
                {
                    name: '可用:45%',
                    y: 45.0,
                    sliced: false,
                    selected: true
                }
            ]
        }]
    });

    $('#container1').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 35,
                beta: 0
            }
        },
        colors:[
                '#D82D3E',
                '#64B5E4'
              ],
        title: {
            text: '硬盘使用率'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: false,
                    format: '{point.name}',
                    //distance:0
                },
                showInLegend: true
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            type: 'pie',
            name: 'Browser share',
            data: [
                ['已用:25%',   25.0],
                {
                    name: '可用:75%',
                    y: 75.0,
                    sliced: false,
                    selected: true
                }
            ]
        }]
    });

     $('#container2').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 35,
                beta: 0
            }
        },
        colors:[
                '#D82D3E',
                '#64B5E4'
              ],
        title: {
            text: 'CPU使用率'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: false,
                    format: '{point.name}',
                    //distance:0
                },
                showInLegend: true
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            type: 'pie',
            name: 'Browser share',
            data: [
                ['已用:20%',   20.0],
                {
                    name: '可用:80%',
                    y: 82.0,
                    sliced: false,
                    selected: true
                }
            ]
        }]
    });
});


