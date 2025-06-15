import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PermissionsSectionComponent } from './permissions-section.component';

describe('PermissionsSectionComponent', () => {
  let component: PermissionsSectionComponent;
  let fixture: ComponentFixture<PermissionsSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PermissionsSectionComponent]
    });
    fixture = TestBed.createComponent(PermissionsSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
