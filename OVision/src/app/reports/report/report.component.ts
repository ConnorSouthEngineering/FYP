import { Component, OnInit, Input } from '@angular/core';
import { TimeSet, CountSet } from 'src/shared/models/DataStructures';
import { GetDataService } from './get-data.service';
import { ActivatedRoute } from '@angular/router';
import { GetGraphService } from './get-graph.service';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.sass']
})
export class ReportComponent implements OnInit {
  reportName: string = "Report";
  id: string | null = "id"
  reportid: string = "reportID";
  dataSets: Array<CountSet | TimeSet> = [];
  visualise: string = "bar-graph";
  chosenDataSet: CountSet | TimeSet = new CountSet("Cooking", 
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
  currentPage: number = 1;
  itemsPerPage: number = 1;
  pageTitle: string = "title";

  constructor(private getDataService: GetDataService,
              private getGraph: GetGraphService,
              private route: ActivatedRoute) { }

  changeTitle(visualise: string) {
    switch(visualise)
    {
      case "line-graph":{
        this.pageTitle = "Activities: "+this.chosenDataSet.actionName;
        break;
      }
      case "bar-graph":{
        this.pageTitle = "Summary";
        break;
      }
    }
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('reportID');
    console.log(this.reportid);
    if(this.id)
      this.reportid = this.id;
      this.getGraph.getGraphType(this.reportid).subscribe({
        next: (graphType) => {
          console.log(graphType);
          this.visualise = graphType;
        },
        error: (error) => console.error('Error fetching data:', error)  
        });
      this.getDataService.getData(this.reportid).subscribe({
        next: (data) => {
          this.dataSets = data;
          this.chosenDataSet = this.dataSets[0];
          this.changeTitle(this.visualise);
        },
        error: (error) => console.error('Error fetching data:', error)
      });
  }

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.chosenDataSet = this.dataSets[this.currentPage-1];
    this.changeTitle(this.visualise)
  }
}

