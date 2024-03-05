import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetGraphService {
  constructor(private http: HttpClient) { }


  getGraphId(_report_id: string): Observable<any[]> {

    const url = `http://localhost:3000/reports/${_report_id}/graph`;

    return this.http.get<any[]>(url);
  }
}
