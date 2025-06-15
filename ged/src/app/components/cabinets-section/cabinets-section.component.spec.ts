import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CabinetsSectionComponent } from './cabinets-section.component';

describe('CabinetsSectionComponent', () => {
  let component: CabinetsSectionComponent;
  let fixture: ComponentFixture<CabinetsSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CabinetsSectionComponent]
    });
    fixture = TestBed.createComponent(CabinetsSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
