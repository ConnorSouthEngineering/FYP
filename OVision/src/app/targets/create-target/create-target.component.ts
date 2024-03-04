import { Component } from '@angular/core';

@Component({
  selector: 'app-create-target',
  templateUrl: './create-target.component.html',
  styleUrls: ['./create-target.component.sass']
})
export class CreateTargetComponent {
selectedTargetType: string = 'Location';

targetName: string = '';
altName: string = '';

access: string = '';

dob: string = '';
role: string = '';

createTarget(){
  
}

onTargetTypeChange() {
  console.log('Selected Target Type:', this.selectedTargetType);
}
}
