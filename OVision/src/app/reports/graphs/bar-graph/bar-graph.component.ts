import { Component, Input, SimpleChanges } from '@angular/core';
import { EChartsOption } from 'echarts';
import { CountSet, TimeSet } from 'src/shared/models/DataStructures';
import { GetMapService } from '../../../passive/get-maps.service';

@Component({
  selector: 'app-bar-graph',
  templateUrl: './bar-graph.component.html',
  styleUrls: ['./bar-graph.component.sass']
})

export class BarGraphComponent {
  @Input() dataSets: CountSet[] | TimeSet[] = 
    [new CountSet(1, 
      [
        "2024-03-25",
        "2024-03-26",
        "2024-03-27"
      ],
      [
        1,
        2,
        3
      ]),
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
        ])
  ];
  avgValues: Array<number> = [];
  activityNames: Array<string> = [];
  chartOption: EChartsOption = {
    xAxis: {
      type: 'category',
      data: ["cooking","cleaning"]
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: [1,2],
        type: 'graph',
        color: ['#503e66']
      },
    ],
    };
  yLabel: string = "Y Label"
    ngOnChanges(changes: SimpleChanges): void {
      if (changes['dataSets']) {
        this.updateChart();
      }
    }

    constructor(private mapService: GetMapService) { }

    
    getClassName() {
      this.mapService.fetchClassMap().subscribe(classMaps => {
        const classMap = classMaps[0]?.get_class_map;
        console.log(classMap);
        if (classMap) {
          this.activityNames = this.dataSets.map(dataSet => {
            const className = classMap[dataSet.classid];
            if (className) {
              return className.charAt(0).toUpperCase() + className.slice(1);
            } else {
              console.log('Class name not found for ID:', dataSet.classid);
              return "Fetch Error";
            }
          });
        }})}

    getAverage()
    {
      this.dataSets.forEach( (element) => {
        this.activityNames.push(element.classid.toString());
        let total = element.values.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
        this.avgValues.push((total/element.values.length));
      })
    }

    private updateChart(): void {
      this.avgValues = [];
      this.activityNames = [];
      this.getAverage();
      this.getClassName();
      if(this.dataSets[0] instanceof TimeSet){
        this.yLabel = "Time (" + this.dataSets[0].metric + ")"
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
          data: this.activityNames,
          name: "Activity",
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
            data: this.avgValues,
            type: 'bar',
            color: ['#BA7489']
          },
        ],
      };
    }
}
