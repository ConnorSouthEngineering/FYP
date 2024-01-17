import { Component, Input } from '@angular/core';
import { actionDataSet } from 'src/shared/models/actionDataSet';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.sass']
})
export class ReportComponent {
  @Input() targetName: string = "Target";
  @Input() dataSets: actionDataSet[] = 
  [
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
                      null),
    new actionDataSet("Cleaning", 
                      [
                        new Date(2022, 4, 2),
                        new Date(2022, 4, 15),
                        new Date(2022, 4, 20)
                      ],
                      "Time",
                      [
                        5,
                        15,
                        10
                      ],
                      "Seconds")  
  ];
  @Input() visualise: string = "line-graph";
  chosenDataSet: actionDataSet = this.dataSets[0];
  currentPage: number = 1;
  itemsPerPage: number = 1;
  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.chosenDataSet = this.dataSets[this.currentPage-1];
  }
}

