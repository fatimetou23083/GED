import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MessagingSectionComponent } from './messaging-section.component';

describe('MessagingSectionComponent', () => {
  let component: MessagingSectionComponent;
  let fixture: ComponentFixture<MessagingSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MessagingSectionComponent]
    });
    fixture = TestBed.createComponent(MessagingSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
