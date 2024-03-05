import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetModelService {
  constructor(private http: HttpClient) { }


  getModelService(itemLimit: number = 10, currentPage: number = 1): Observable<any[]> {

    const url = 'http://localhost:3000/models/';

    const params = new HttpParams()
      .set('itemLimit', itemLimit.toString())
      .set('currentPage', currentPage.toString());

    return this.http.get<any[]>(url, { params });
  }
}
