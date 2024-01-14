import { Component } from '@angular/core';
import { actionDataSet } from 'src/shared/models/actionDataSet';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.sass']
})
export class ReportComponent {
targetName: string = "Corridor";
dataSets: actionDataSet[] = [
  new actionDataSet("cooking", [new Date(2022, 2, 4),
                              new Date(2022, 2, 5),
                              new Date(2022, 2, 6)],
                              [1,2,3])
  ]
}

