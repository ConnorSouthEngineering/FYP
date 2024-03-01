import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, interval } from 'rxjs';
import { catchError, startWith, switchMap, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class GetMapService {
  private classMapUrl = 'http://localhost:3000/maps/class';
  private graphMapUrl = 'http://localhost:3000/maps/graphs';
  private countMapUrl = 'http://localhost:3000/maps/counts';
  private refreshInterval = 30 * 60 * 1000;

  constructor(private http: HttpClient) {
    console.log('MapService initialized'); 
    this.initiatePeriodicRefresh();
  }

  private fetchAndCache(url: string, cacheKey: string): Observable<any> {
    return this.http.get<any[]>(url).pipe(
      tap(data => {
        console.log(`Data fetched and cached for ${cacheKey}`, data);
        localStorage.setItem(cacheKey, JSON.stringify(data));
      }),
      catchError(error => {
        console.error(`Error fetching data from ${url}:`, error);
        return of(null);
      })
    );
  }

  initiatePeriodicRefresh() {
    interval(this.refreshInterval).pipe(
      startWith(0),
      switchMap(() => {
        console.log('Refreshing classMap data'); 
        return this.fetchAndCache(this.classMapUrl, 'classMap');
      })
    ).subscribe();

    interval(this.refreshInterval).pipe(
      startWith(0),
      switchMap(() => {
        console.log('Refreshing graphMap data'); 
        return this.fetchAndCache(this.graphMapUrl, 'graphMap');
      })
    ).subscribe();

    interval(this.refreshInterval).pipe(
      startWith(0),
      switchMap(() => {
        console.log('Refreshing countMap data'); 
        return this.fetchAndCache(this.countMapUrl, 'countMap');
      })
    ).subscribe();
  }

  fetchClassMap(): Observable<any> {
    const cachedData = localStorage.getItem('classMap');
    if (cachedData) {
      console.log('Fetching classMap from cache'); 
      return of(JSON.parse(cachedData));
    } else {
      console.log('Fetching classMap from server');
      return this.fetchAndCache(this.classMapUrl, 'classMap');
    }
  }

  fetchCountMap(): Observable<any> {
    const cachedData = localStorage.getItem('countMap');
    if (cachedData) {
      console.log('Fetching countMap from cache'); 
      return of(JSON.parse(cachedData));
    } else {
      console.log('Fetching countMap from server');
      return this.fetchAndCache(this.countMapUrl, 'countMap');
    }
  }

  fetchGraphMap(): Observable<any> {
    const cachedData = localStorage.getItem('graphMap');
    if (cachedData) {
      console.log('Fetching graphMap from cache'); 
      return of(JSON.parse(cachedData));
    } else {
      console.log('Fetching graphMap from server');
      return this.fetchAndCache(this.graphMapUrl, 'graphMap');
    }
  }
}
