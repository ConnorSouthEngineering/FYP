import { Component } from '@angular/core';
import { CreateTargetService } from './create-target.service';
import { Location, Person, Target } from 'src/shared/models/Entities';

@Component({
  selector: 'app-create-target',
  templateUrl: './create-target.component.html',
  styleUrls: ['./create-target.component.sass']
})
export class CreateTargetComponent {
selectedTargetType: string = 'Location';

target_name: Target['target_name'] = '';
alt_name: Target['alt_name'] = '';

access: Location['access'] = null;

dob_entry: string = '';
role: Person['role'] = '';

constructor(private createTarget: CreateTargetService) { }

checkInputs()
{
  let errors: string[] = [];
  if (!this.target_name.trim()) {
    errors.push('Target Name must not be empty.');
  }
  if (!this.alt_name.trim()) {
    errors.push('Alt Name must not be empty.');
  }
  if (this.selectedTargetType === 'Location') {
    if (this.access !== 'public' && this.access !== 'private') {
      errors.push('Access must be "public", "private"');
    }
    return errors;
  }
  else{
    if (!this.role.trim()) {
      errors.push('Role must be defined');
    }
    return errors;
  }
  return null;
}

createPerson() {
  const errors = this.checkInputs();
  const new_person = new Person(9999, this.target_name, this.alt_name, new Date(), 'New', new Date(this.dob_entry), this.role);
  console.log(new_person)
  /*   this.createTarget.postPerson(person).subscribe({
    next: (response) => console.log(response),
    error: (error) => console.error('Error:', error),
  }); */
}

createLocation() {
  this.checkInputs();
  const new_location = new Location(9999, this.target_name, this.alt_name, new Date(), 'New', this.access);
  console.log(new_location)
/*   this.createTarget.postLocation(location).subscribe({
    next: (response) => console.log(response),
    error: (error) => console.error('Error:', error),
  }); */
}

onTargetTypeChange() {
  console.log('Selected Target Type:', this.selectedTargetType);
}
}
