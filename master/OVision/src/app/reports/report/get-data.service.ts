import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})
export class GetDataService {
  constructor(private http: HttpClient) { }

  getDataService(_report_id: string, _start_date: Date, _end_date: Date, _class_ids: any[], _deployment_id: number, _metric_value: string | null): Observable<any[]> {
    const url = `http://localhost:3000/reports/${_report_id}/data`;
  
    let classIdsString = JSON.stringify(_class_ids);
  
    let params = new HttpParams()
      .set('_start_date', _start_date.toISOString()) 
      .set('_end_date', _end_date.toISOString())
      .set('_class_ids', classIdsString) 
      .set('_deployment_id', _deployment_id.toString());
  
    if (_metric_value !== null) {
      params = params.set('_metric_value', _metric_value);
    }
    console.log(params.toString());
    return this.http.get<any[]>(url, { params: params });
  }  
}