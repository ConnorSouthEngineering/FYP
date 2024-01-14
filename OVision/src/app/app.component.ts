import { Component, OnInit } from '@angular/core';
import { deploymentItem } from 'src/shared/models/deploymentItem';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent implements OnInit {
  title = 'OVision';
  deploymentSessions: deploymentItem[] = [
    new deploymentItem("Corridor", "Active", 1, "IBM MIT", new Date(2022, 2, 3), new Date(2024, 2, 20), "address", "address"),
    new deploymentItem("Reception", "Error", 3, "Toyota Activity", new Date(2022, 5, 2), new Date(2022, 6, 11), "address", "address"),
    new deploymentItem("Kitchen", "Expiring", 2, "YOLOv8", new Date(2013, 2, 6), new Date(2024, 2, 20), "address", "address"),
    new deploymentItem("Hall", "Active", 5, "Microsoft COCO", new Date(2010, 2, 12), new Date(2022, 1, 16), "address", "address")
  ];
  displayedSessions: deploymentItem[] = [];
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
