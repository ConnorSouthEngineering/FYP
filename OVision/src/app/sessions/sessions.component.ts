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
    console.log("Updating pages")
    this.fetchDeployments();
  } 

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.updateDisplayedSessions();
  }

  fetchDeployments() {
    console.log("Fetching deployments")
    this.getDeploymentsService.getDeployments(this.itemsPerPage, this.currentPage).subscribe({
      next: (data: any[]) => {
        console.log("Fetched data:", data);
        const deployments = data.flatMap(item => item.get_latest_deployments).map(deployment => {
          return new Deployment(
            deployment.deployment_id.toString(), 
            deployment.deployment_name,
            deployment.target_id.toString(),
            deployment.status_value,
            deployment.model_id.toString(),
            new Date(deployment.creation_date), 
            new Date(deployment.start_date),
            new Date(deployment.expiry_date)
          );
        });
        this.deploymentSessions = deployments;
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
