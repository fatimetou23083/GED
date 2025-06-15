import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowsSectionComponent } from './workflows-section.component';

describe('WorkflowsSectionComponent', () => {
  let component: WorkflowsSectionComponent;
  let fixture: ComponentFixture<WorkflowsSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowsSectionComponent]
    });
    fixture = TestBed.createComponent(WorkflowsSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
