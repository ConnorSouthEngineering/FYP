import { Component } from '@angular/core';
import { CreateTargetService } from './create-target.service';
import { Location, Person, Target } from 'src/shared/models/Entities';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-create-target',
  templateUrl: './create-target.component.html',
  styleUrls: ['./create-target.component.sass']
})
export class CreateTargetComponent {
selectedTargetType: string = 'Choose Target Type';

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
      errors.push('Access must be "public" or "private"');
    }
  }
  else if(this.selectedTargetType === 'Person') {
    if (!this.role.trim()) {
      errors.push('Role must not be empty');
    }
  }    
  return errors;
}

checkDate(){

  const parts = this.dob_entry.split('/'); 
  return new Date(parseInt(parts[2]), parseInt(parts[1])-1, parseInt(parts[0])); 
}

createPerson() {
  const errors = this.checkInputs();
  if( errors.length === 0){
    console.log(this.dob_entry)
    const dob = this.checkDate();
    const new_person = new Person(9999, this.target_name, this.alt_name, new Date(), 'New', new Date(dob), this.role);
    console.log(new_person);
    this.createTarget.postPerson(new_person).subscribe({
      next: (response) => console.log(response),
      error: (error) => console.error('Error:', error),});
  }
  else
  {
    console.log(errors)
  }
}

createLocation() {
  const errors = this.checkInputs();
  if( errors.length === 0 ){
    const new_location = new Location(9999, this.target_name, this.alt_name, new Date(), 'New', this.access);
    console.log(new_location)
    this.createTarget.postLocation(new_location).subscribe({
      next: (response) => console.log(response),
      error: (error) => console.error('Error:', error),
    });
  }
  else
  {
    console.log(errors)
  }
}

}
