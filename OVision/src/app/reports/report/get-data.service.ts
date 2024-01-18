import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, switchMap, map, of } from 'rxjs';
import { TimeSet,CountSet } from 'src/shared/models/DataStructures';
@Injectable({
  providedIn: 'root'
})
export class GetDataService {
  constructor(private http: HttpClient) { }
  getData(reportId: string): Observable<Array<CountSet | TimeSet>> {

    return this.http.get<any[]>('assets/db-standin/reports.JSON').pipe(switchMap(reports => {
        const report = reports.find(r => r[0] === reportId);

        if (!report) return of([]);
        const requiredActivities = report[8];
        const deploymentid = report[2];

        return this.http.get<any[]>('assets/db-standin/data.JSON').pipe(map(deploymentData => {
            const dataForDeployment = deploymentData.find(([id, _]) => id === deploymentid);

            if (!dataForDeployment) return [];
            const activitiesData = dataForDeployment[1];

            const filteredData = activitiesData.filter((activityData: any[]) => requiredActivities.includes(activityData[0])).map((activityData: string | any[]) => {
              if (activityData.length === 4) {
                return new TimeSet(activityData[0], activityData[1], activityData[2], activityData[3]);
                } 
              else {
                return new CountSet(activityData[0], activityData[1], activityData[2]);
                }
                });

            return filteredData
          })
        );
      })
    );
  }
}
