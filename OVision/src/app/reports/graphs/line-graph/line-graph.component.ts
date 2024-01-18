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
    new CountSet("Cooking", 
    [
      1651449600,
      1652572800,
      1646524800
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
      const formattedDates = this.dataSet.dateValues.map(date => 
        `${(new Date(date*1000)).getDate()}/${(new Date(date*1000)).getMonth() + 1}` 
      );
      
      if(this.dataSet instanceof TimeSet){
        this.yLabel = "Time (" + this.dataSet.timeUnit + ")"
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
            data: this.dataSet.values,
            type: 'line',
            color: ['#BA7489']
          },
        ],
      };
    }
}
