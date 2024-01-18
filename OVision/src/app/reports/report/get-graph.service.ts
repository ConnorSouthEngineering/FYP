import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, switchMap, of } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class GetGraphService {

  constructor(private http: HttpClient) { }
  getGraphType(reportId: string): Observable<string> {
    return this.http.get<any[]>('assets/db-standin/reports.JSON').pipe(
        switchMap(reports => {
            const report = reports.find(r => r[0] === reportId);
            return of(report[7]); 
        })
    );
}
}
