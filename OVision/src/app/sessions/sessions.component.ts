import { Component, OnInit } from '@angular/core';
import { GetDeploymentsService } from './get-deployments.service';
import { Deployment } from 'src/shared/models/Entities';

@Component({
  selector: 'app-sessions',
  templateUrl: './sessions.component.html',
  styleUrls: ['./sessions.component.sass']
})
export class SessionsComponent implements OnInit {
  deploymentSessions: Deployment[] = [];
  displayedSessions: Deployment[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 2;

  constructor(private getDeploymentsService: GetDeploymentsService) { }

  ngOnInit() {
    this.getDeploymentsService.getDeployments().subscribe({
      next: (data: any[]) => {
        console.log("Fetched data:", data);
        this.deploymentSessions = data.map(item => new Deployment(
          item[0], 
          item[1], 
          item[2], 
          item[3], 
          item[4], 
          new Date(item[5] * 1000), 
          new Date(item[6] * 1000)  
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
