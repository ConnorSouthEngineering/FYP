import { Component } from '@angular/core';

@Component({
  selector: 'app-create-target',
  templateUrl: './create-target.component.html',
  styleUrls: ['./create-target.component.sass']
})
export class CreateTargetComponent {
test: boolean = false;
selectedTargetType: string = 'Choose Target Type';
targetName: string = '';
onTargetTypeChange() {
  console.log('Selected Target Type:', this.selectedTargetType);
}
}
