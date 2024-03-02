import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateDeploymentComponent } from './create-deployment.component';

describe('CreateDeploymentComponent', () => {
  let component: CreateDeploymentComponent;
  let fixture: ComponentFixture<CreateDeploymentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateDeploymentComponent]
    });
    fixture = TestBed.createComponent(CreateDeploymentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
