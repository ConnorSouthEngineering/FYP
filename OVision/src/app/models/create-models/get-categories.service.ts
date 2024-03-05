import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetCategoriesService {
  constructor(private http: HttpClient) { }


  getCategories(): Observable<any[]> {

    const url = 'http://localhost:3000/models/categories/';

    return this.http.get<any[]>(url);
  }
}
