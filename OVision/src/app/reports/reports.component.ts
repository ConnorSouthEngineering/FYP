import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges } from '@angular/core';
import { GetReportsService } from './get-reports.service';
import { Report } from 'src/shared/models/Entities';
@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.sass']
})

export class ReportsComponent {
  deploymentSessions: Report[] = [];
  displayedSessions: Report[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 2;

  constructor(private getReportsService: GetReportsService) { }

  ngOnInit() {
    this.getReportsService.getReports().subscribe({
      next: (data: any[]) => {
        console.log("Fetched data:", data);
        this.deploymentSessions = data.map(item => new Report(
          item[0], 
          item[1], 
          item[2], 
          item[3],
          item[4],
          new Date(item[5] * 1000), 
          new Date(item[6] * 1000),
          item[7],
          item[8]
        ));
        this.updateDisplayedSessions();
      },
      error: (error) => console.error('Error fetching deployments:', error)
    });
  }

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.updateDisplayedSessions();
  }

  updateDisplayedSessions() {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.displayedSessions = this.deploymentSessions.slice(startIndex, endIndex);
  }
}
