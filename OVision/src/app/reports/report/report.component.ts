import { Component, OnInit, Input, ErrorHandler } from '@angular/core';
import { TimeSet, CountSet } from 'src/shared/models/DataStructures';
import { GetDataService } from './get-data.service';
import { ActivatedRoute } from '@angular/router';
import { GetGraphService } from './get-graph.service';
import { GetMapService } from '../../passive/get-maps.service';
import { GetReportService } from './get-report.service';
import { GetReportClassesService} from './get-report-classes.service';
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';

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
  visualise: string = "bar";
  chosenDataSet: CountSet | TimeSet = new CountSet(1, 
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
  currentPage: number = 1;
  itemsPerPage: number = 1;
  pageTitle: string = "title";

  constructor(private getGraph: GetGraphService,
              private route: ActivatedRoute,
              private mapService: GetMapService,
              private getReport: GetReportService,
              private getReportClasses: GetReportClassesService,
              private getData: GetDataService
              ) { }

  changeTitle(visualise: string) {
    switch(visualise)
    {
      case "line":{
        console.log("line")
        this.getClassName();
        break;
      }
      case "bar":{
        console.log("bar")
        this.pageTitle = "Summary";
        break;
      }
    }
  }

  ngOnInit() {
      this.getGraphType();
      this.getReportData();
  }

  getClassName(){
    this.mapService.fetchClassMap().subscribe(classMaps => {
      const classMap = classMaps[0]?.get_class_map;
      console.log(classMap)
      if (classMap) {
        const className = classMap[this.chosenDataSet.classid];
        if (className) {
          this.pageTitle ="Activity: "+className.charAt(0).toUpperCase() + className.slice(1);;
        } else {
          console.log('Class name not found for ID:', this.chosenDataSet.classid);
          this.pageTitle = "Fetch Error"
        }
      }})};


  getGraphType(){
    this.id = this.route.snapshot.paramMap.get('reportID');
    if (this.id) {
      this.reportid = this.id;
      this.getGraph.getGraphId(this.reportid).subscribe({
        next: (graph_id) => {
          console.log(graph_id);
          this.mapService.fetchGraphMap().subscribe(graphMaps => {
            const graphMap = graphMaps[0]?.get_graph_map;
            if (graphMap) {
              const graphType = graphMap[graph_id[0]?.get_graph_id];
              if (graphType) {
                this.visualise = graphType;
                this.changeTitle(this.visualise);
              } else {
                console.log('Graph type not found for ID:', graph_id[0]?.get_graph_id);
              }
            } else {
              console.error('Graph map not found in the fetched data.');
            }
          });
        },
        error: (error) => console.error('Error fetching data:', error)  
      });
    }
  }
  

  getReportData() {
    this.getReport.getReportData(this.reportid).pipe(
      switchMap(report => {
        this.reportName = report[0]?.get_report[0]?.report_name;
        let frequencyUnit = report[0]?.get_report[0]?.frequency_unit;
        let frequencyValue = report[0]?.get_report[0]?.frequency_value;
        let deploymentId = report[0]?.get_report[0]?.deployment_id;
        let startDate = this.calculateStartDate(frequencyUnit, frequencyValue);
        let endDate = new Date("2024-03-30"); //new Date("2024-03-30"); set to this format to test data that is longer than X amount of time ago
        return this.getClasses().pipe(
          switchMap(classes => {
            return this.getData.getDataService(this.reportid, startDate, endDate, classes, deploymentId, null);
          })
        );
      })
    ).subscribe({
      next: (data) => {
        console.log(data)
        this.dataSets = this.mapJsonToDataSets(data);
      },
      error: (error) => console.error('Error fetching report data:', error)
    });
  }
  
  mapJsonToDataSets(jsonData: any[]){
    let tempDataSet: (CountSet | TimeSet)[] = [];
    jsonData.forEach(item => {
      item.get_report_data.forEach((data: any) => {
        if (data.metric === null) {
          tempDataSet.push(new CountSet(data.classid, data.creation_dates, data.values));
        } else {
          tempDataSet.push(new TimeSet(data.classid, data.creation_dates, data.values, data.metric));
        }
      });
    });
    return tempDataSet;
  }

  getClasses(): Observable<any[]> {
    return new Observable(subscriber => {
      this.id = this.route.snapshot.paramMap.get('reportID');
      if (this.id) {
        this.reportid = this.id;
        this.getReportClasses.getClasses(this.reportid).subscribe({
          next: (response) => {
            console.log(response);
            const classesArray = response[0]?.get_report_classes?.classes;
            if (classesArray) {
              subscriber.next(classesArray);
            } else {
              console.log('Classes array not found in the response');
              subscriber.next([]); 
            }
          },
          error: (error) => {
            console.error('Error fetching classes:', error);
            subscriber.error(error);
          },
          complete: () => subscriber.complete()
        });
      } else {
        subscriber.next([]);
      }
    });
  }
  
  
  calculateStartDate(frequencyUnit: string, frequencyValue: number) {
    let startDate = new Date();
    switch (frequencyUnit) {
      case 'day':
        startDate.setDate(startDate.getDate() - frequencyValue);
        break;
      case 'week':
        startDate.setDate(startDate.getDate() - (frequencyValue * 7));
        break;
      case 'month':
        startDate.setMonth(startDate.getMonth() - frequencyValue);
        break;
      case 'year':
        startDate.setFullYear(startDate.getFullYear() - frequencyValue);
        break;
      default:
        console.log('Invalid frequency unit:', frequencyUnit);
    }
    return startDate;
  }

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.chosenDataSet = this.dataSets[this.currentPage-1];
    this.changeTitle(this.visualise)
  }
}

