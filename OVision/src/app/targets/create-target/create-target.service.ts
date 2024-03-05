import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Person, Location } from '../../../shared/models/Entities'

@Injectable({
  providedIn: 'root'
})
export class CreateTargetService {
  constructor(private http: HttpClient) { }
  apiUrl = 'http://localhost:3000/targets/create';

  postPerson(person: Person) {
    const url = `${this.apiUrl}`;
    return this.http.post(url, person);
  }

  postLocation(location: Location) {
    const url = `${this.apiUrl}`;
    return this.http.post(url, location);
  }
}