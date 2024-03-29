import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class GetReportClassesService {

  constructor(private http: HttpClient) { }


  getClasses(_report_id: string): Observable<any[]> {

    const url = `http://localhost:3000/reports/id/${_report_id}/classes`;

    return this.http.get<any[]>(url);
  }
}
