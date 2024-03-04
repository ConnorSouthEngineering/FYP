import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {Target} from '../../../shared/models/Entities'

@Injectable({
  providedIn: 'root'
})
export class CreateTargetService {
  constructor(private http: HttpClient) { }


  createTargetService(target: Target): Observable<Target> {

    const url = 'http://localhost:3000/targets/create';
    new 
    const params = new HttpParams()
      .set('itemLimit', itemLimit.toString())
      .set('currentPage', currentPage.toString());

    return this.http.post<target>(url, { params });
  }
}