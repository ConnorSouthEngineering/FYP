import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Report } from 'src/shared/models/Entities';

@Injectable({
  providedIn: 'root'
})
export class GetReportsService {
  constructor(private http: HttpClient) { }

  getReports(): Observable<any[]> {
    return this.http.get<any[]>('assets/db-standin/reports.JSON');
  }
}
