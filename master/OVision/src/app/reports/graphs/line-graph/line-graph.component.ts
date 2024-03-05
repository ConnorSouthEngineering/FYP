import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { EChartsOption } from 'echarts';
import { TimeSet, CountSet } from 'src/shared/models/DataStructures';
@Component({
  selector: 'app-line-graph',
  templateUrl: './line-graph.component.html',
  styleUrls: ['./line-graph.component.sass']
})
export class LineGraphComponent {
  @Input() dataSet: CountSet | TimeSet = 
  new CountSet(1, 
    [
      "2024-03-25",
      "2024-03-26",
      "2024-03-27"
    ],
    [
      1,
      2,
      3
    ]);

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
      console.log(this.dataSet)
      
      if(this.dataSet instanceof TimeSet){
        this.yLabel = "Time (" + this.dataSet.metric + ")"
      }
      else
      {
        this.yLabel = "Count"
      }

      this.chartOption = {
        grid:{
          backgroundColor: 'white',
          show: true,
        },
        xAxis: {
          type: 'category',
          data: this.dataSet.dateValues,
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
            data: this.dataSet.values,
            type: 'line',
            color: ['#BA7489']
          },
        ],
      };
    }
}
