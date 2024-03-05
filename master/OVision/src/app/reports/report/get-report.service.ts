import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class GetReportService {

  constructor(private http: HttpClient) { }


  getReportData(_report_id: string): Observable<any[]> {

    const url = `http://localhost:3000/reports/${_report_id}`;

    return this.http.get<any[]>(url);
  }
}
