import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsersSectionComponent } from './users-section.component';

describe('UsersSectionComponent', () => {
  let component: UsersSectionComponent;
  let fixture: ComponentFixture<UsersSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UsersSectionComponent]
    });
    fixture = TestBed.createComponent(UsersSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
