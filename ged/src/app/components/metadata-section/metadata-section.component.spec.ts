import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetadataSectionComponent } from './metadata-section.component';

describe('MetadataSectionComponent', () => {
  let component: MetadataSectionComponent;
  let fixture: ComponentFixture<MetadataSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MetadataSectionComponent]
    });
    fixture = TestBed.createComponent(MetadataSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
