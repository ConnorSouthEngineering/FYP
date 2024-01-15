import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { EChartsOption } from 'echarts';
import { actionDataSet } from 'src/shared/models/actionDataSet';
@Component({
  selector: 'app-line-graph',
  templateUrl: './line-graph.component.html',
  styleUrls: ['./line-graph.component.sass']
})
export class LineGraphComponent {
  @Input() dataSet = 
    new actionDataSet("Cooking", 
                      [
                        new Date(2022, 2, 4),
                        new Date(2022, 2, 5),
                        new Date(2022, 2, 6)
                      ],
                      "Count",
                      [
                        1,
                        2,
                        3
                      ],
                      null);

  chartOption: EChartsOption = {
    xAxis: {
      type: 'category',
      data: ["01/02","02/02","03/02"]
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: [1,2,3],
        type: 'line',
        color: ['#503e66']
      },
    ],
    };
  yLabel: string = "Y Label"
    ngOnChanges(changes: SimpleChanges): void {
      if (changes['dataSet']) {
        this.updateChart();
      }
    }

    private updateChart(): void {
      const formattedDates = this.dataSet.dateValues.map(date => 
        `${date.getDate()}/${date.getMonth() + 1}` // Month is 0-indexed
      );
      
      if(this.dataSet.metricUnit == null){
        this.yLabel = this.dataSet.metricType
      }
      else
      {
        this.yLabel = this.dataSet.metricType + this.dataSet.metricUnit
      }

      this.chartOption = {
        grid:{
          backgroundColor: 'white',
          show: true,
        },
        xAxis: {
          type: 'category',
          data: formattedDates,
          name: "Dates",
          nameLocation: 'middle',
          nameTextStyle: {color: '#BA7489', fontSize: '20', fontWeight: 'bold', verticalAlign: 'bottom',padding: [0,0,-30,0]},
          axisLabel:{color: '#BA7489', fontSize: '15'}
        },     
        yAxis: {
          type: 'value',
          name: this.yLabel,
          nameLocation: 'middle',
          nameTextStyle: {color: '#BA7489',fontSize: '20', fontWeight: 'bold', verticalAlign: 'bottom',padding: [0,0,30,0]},
          axisLabel:{color: '#BA7489', fontSize: '15'}
        },
        series: [
          {
            data: this.dataSet.metricValue,
            type: 'line',
            color: ['#BA7489']
          },
        ],
      };
    }
}
