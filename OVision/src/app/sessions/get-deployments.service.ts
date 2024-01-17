import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Deployment } from 'src/shared/models/Entities';

@Injectable({
  providedIn: 'root'
})
export class GetDeploymentsService {
  constructor(private http: HttpClient) { }

  getDeployments(): Observable<any[]> {
    return this.http.get<any[]>('assets/db-standin/deployments.JSON');
  }
}
