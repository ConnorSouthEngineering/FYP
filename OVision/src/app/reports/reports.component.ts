import { Component, OnInit } from '@angular/core';
import { GetReportsService } from './get-reports.service';
import { Report } from 'src/shared/models/Entities';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.sass']
})
export class ReportsComponent implements OnInit {
  deploymentSessions: Report[] = [];
  displayedSessions: Report[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 2;

  constructor(private getReportsService: GetReportsService) { }

  ngOnInit() {
    this.fetchReports();
  }

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.fetchReports(); 
  }

  fetchReports() {
    this.getReportsService.getReports(this.itemsPerPage, this.currentPage).subscribe({
      next: (data: any[]) => {
        this.deploymentSessions = data.flatMap(item => item.get_latest_reports).map(report => new Report(
          report.report_id.toString(), 
          report.report_name,
          report.deployment_id.toString(),
          report.frequency_value,
          report.frequency_unit,
          new Date(report.creation_date), 
          report.last_gen ? new Date(report.last_gen) : null,
          report.graph_id
        ));
        this.updateDisplayedSessions();
      },
      error: (error) => console.error('Error fetching deployments:', error)
    });
  }

  updateDisplayedSessions() {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.displayedSessions = this.deploymentSessions.slice(startIndex, endIndex);
  }
}
