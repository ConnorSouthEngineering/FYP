import { Component, OnInit } from '@angular/core';
import { GetTargetService } from './get-targets.service';
import { Location, Person, Target } from 'src/shared/models/Entities';

@Component({
  selector: 'app-targets',
  templateUrl: './targets.component.html',
  styleUrls: ['./targets.component.sass']
})
export class TargetComponent implements OnInit {
  persons: Person[] = [];
  locations: Location[] = []
  displayedPersons: Person[] = [];
  displayedLocations: Location[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 2;
  maxLength: number = 1
  constructor(private getTargetService: GetTargetService) { }

  ngOnInit() {
    console.log("Updating pages")
    this.fetchTargets();
  } 

  onPageChange(newPage: number) {
    this.currentPage = newPage;
    console.log(this.currentPage)
    this.updateDisplayedSessions();
  }

  fetchTargets() {
    console.log("Fetching Targets");
    this.getTargetService.getTargetService(this.itemsPerPage, this.currentPage).subscribe({
      next: (data: any[]) => {
        console.log("Fetched data:", data);

        this.persons = [];
        this.locations = [];
        data.flatMap(item => item.get_latest_targets).forEach(target => {
          if (target.dob !== null) {
            console.log(target.target_id)
            this.persons.push(new Person(
              target.target_id,
              target.target_name,
              target.alt_name,
              new Date(target.creation_date),
              target.status_value,
              new Date(target.dob),
              target.role
            ));
          } else {
            this.locations.push(new Location(
              target.target_id,
              target.target_name,
              target.alt_name,
              new Date(target.creation_date),
              target.status_value,
              target.access
            ));
          }
        });
        this.maxLength = Math.max(this.persons.length, this.locations.length);
        console.log("max length:"+this.maxLength)
        this.updateDisplayedSessions();
      },
      error: (error) => console.error('Error fetching targets:', error)
    });
  }

  updateDisplayedSessions() {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.displayedPersons = this.persons.slice(startIndex, endIndex);
    this.displayedLocations = this.locations.slice(startIndex, endIndex);
  }
}
