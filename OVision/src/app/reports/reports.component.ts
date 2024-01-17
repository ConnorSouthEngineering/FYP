import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges } from '@angular/core';
import { Report } from 'src/shared/models/Entities';
@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.sass']
})

export class ReportsComponent {
  deploymentSessions: Report[] = [
    new Report("Activity Counts", "D1234", 2, "week", new Date(2022, 2, 3), new Date(2024, 2, 20)),
    new Report("Visiting Activity", "D324", 1, "month", new Date(2022, 5, 2), new Date(2022, 6, 11)),
    new Report("Culnary Activity", "D554", 3, "week", new Date(2013, 2, 6), new Date(2024, 2, 20)),
    new Report("Passage Count", "D643", 4, "day", new Date(2010, 2, 12), new Date(2022, 1, 16))
  ];
  displayedSessions: Report[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 2;

  ngOnInit() {
    this.updateDisplayedSessions();
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
