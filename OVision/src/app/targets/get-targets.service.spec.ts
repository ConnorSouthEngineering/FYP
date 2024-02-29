import { TestBed } from '@angular/core/testing';

import { GetTargetsService } from './get-targets.service';

describe('GetTargetsService', () => {
  let service: GetTargetsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetTargetsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
