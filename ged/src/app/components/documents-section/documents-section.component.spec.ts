import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentsSectionComponent } from './documents-section.component';

describe('DocumentsSectionComponent', () => {
  let component: DocumentsSectionComponent;
  let fixture: ComponentFixture<DocumentsSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DocumentsSectionComponent]
    });
    fixture = TestBed.createComponent(DocumentsSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
