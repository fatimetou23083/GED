import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatalogSectionComponent } from './catalog-section.component';

describe('CatalogSectionComponent', () => {
  let component: CatalogSectionComponent;
  let fixture: ComponentFixture<CatalogSectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CatalogSectionComponent]
    });
    fixture = TestBed.createComponent(CatalogSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
