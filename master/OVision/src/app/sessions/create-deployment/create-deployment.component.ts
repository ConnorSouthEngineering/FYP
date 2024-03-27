import { ChangeDetectorRef, Component } from '@angular/core';
import { GetMapService } from '../../passive/get-maps.service';
import { GetTargetService } from '../../targets/get-targets.service';
import { GetCategoriesService } from '../../models/create-models/get-categories.service';
import { GetModelService } from '../../models/get-models.service';
import { HandleTaskService } from '../../models/create-models/handle-task.service';
import { Target, Location, Person, Model, ModelConfig } from '../../../shared/models/Entities';
type Map = { [key: string]: string };

@Component({
  selector: 'app-create-deployment',
  templateUrl: './create-deployment.component.html',
  styleUrls: ['./create-deployment.component.sass']
})
export class CreateDeploymentComponent { 

  ngOnInit() {
    console.log("Updating pages")
    this.fetchClassMap();
    this.fetchCategoryMap();
    this.fetchTargetCount();
    this.fetchTargets();
    this.fetchModelCount();
    this.fetchModel();
    this.fetchConfigurationMap();
  } 

  modelName: string = '';
  models: Model[] | null = null;
  selectedModel: Model | null = null;
  configMap: ModelConfig[] = [];
  modelConfiguration: string = '';

  placeHolder: boolean = false;
  targetButtonStatus: boolean = false;
  modelButtonStatus: boolean = true;
  nodeButtonStatus: boolean = true;  
  deviceButtonStatus: boolean = true

  displayOptionsTarget: boolean = true;
  displayOptionsModel: boolean = false;
  displayOptionsNode: boolean = false;
  displayOptionsDevice: boolean = false;
  
  persons: Person[] = [];
  locations: Location[] = [];
  selectedTarget: Target | null = null;
  selectedPerson: Person | null = null;
  personAge: number = 1;
  selectedLocation: Location | null = null;

  currentPage: number = 1;
  itemsPerPage: number = 8;
  maxLength: number = 1;

  phase1: boolean = true;
  nextButtonStatus: boolean = true;
  previousButtonStatus: boolean = true;
  
  classMap: Map | null = null;
  categoryMap: Map | null = null;

  categorisedClasses: any[] = [];
  categorisedClassesString: Map | null = null;
  categories: string[] = [];
  categoriesExpanded: boolean[] = [];

  constructor(private cdr: ChangeDetectorRef,
    private mapService: GetMapService,
    private categoriesService: GetCategoriesService,
    private getTargetService: GetTargetService,
    private getModels: GetModelService
    ) { }

    //Selection Functions
    updateTargetSelection(target: Person | Location){
      this.selectedTarget = target;
      if (target instanceof Location)
      {
        this.selectedLocation = target;
        this.selectedPerson = null;
      }
      else if (target instanceof Person)
      {
        this.selectedPerson = target;
        this.selectedLocation = null;
        this.personAge = target.getAge(target.dob)
      }
      this.modelButtonStatus = false;
    }

    updateModelSelection(model: Model){
      this.selectedModel = model;
      this.nodeButtonStatus = false;
      this.modelConfiguration = this.mapModelConfiguration(this.selectedModel)
    }

    //Display Functions
    selectTarget(){
      this.displayOptionsNode = false;
      this.displayOptionsDevice = false;
      this.displayOptionsModel = false;

      this.displayOptionsTarget = true;
    }
    selectModel(){
      this.displayOptionsNode = false;
      this.displayOptionsDevice = false;
      this.displayOptionsTarget = false;
      
      this.displayOptionsModel = true;
    }

    onPageChange(newPage: number) {
      this.currentPage = newPage;
      console.log(this.currentPage)
      this.fetchTargets();
      console.log(this.selectedTarget)
    }

    //Target Functions
    fetchTargetCount(){
      this.mapService.fetchCountMap().subscribe(countMaps => {
        const countMap = countMaps[0]?.get_count_map;
        if (countMap) {
          console.log("Map:"+countMap);
          console.log("Max Length Map:"+countMap['target_count']);
          this.maxLength = countMap['target_count'];
          console.log("Max Length Saved:"+this.maxLength)
          this.cdr.detectChanges();
        } else {
          console.log('Count not retrieved');
        }
      });
    }
    
    fetchTargets() {
      console.log("Fetching Targets");
      this.getTargetService.getTargetService(this.itemsPerPage, this.currentPage).subscribe({
        next: (data: any[]) => {
          console.log("Fetched data:", data);
  
          this.persons = [];
          this.locations = [];
          data.flatMap(item => item.get_latest_targets).forEach(target => {
          if(target){
              if (target.dob !== null) {
                this.persons.push(new Person(
                  target.target_id,
                  target.target_name,
                  target.alt_name,
                  new Date(target.creation_date),
                  target.status_value,
                  new Date(target.dob),
                  target.role
                ));
              } 
              else {
                this.locations.push(new Location(
                  target.target_id,
                  target.target_name,
                  target.alt_name,
                  new Date(target.creation_date),
                  target.status_value,
                  target.access
                ));
              }
            }
          });
        },
        error: (error) => console.error('Error fetching targets:', error)
      });
    }
    
    //Model Functions

    fetchModelCount(){
      this.mapService.fetchCountMap().subscribe(countMaps => {
        console.log(countMaps);
        console.log(countMaps[0])
        const countMap = countMaps[0]?.get_count_map;
        if (countMap) {
          console.log("Map:"+countMap);
          console.log("Max Length Map:"+countMap['model_count']);
          this.maxLength = countMap['model_count'];
          console.log("Max Length Saved:"+this.maxLength)
          this.cdr.detectChanges();
        } else {
          console.log('Count not retrieved');
        }
      });
    }

    fetchModel() {
      console.log("Fetching Models");
      this.getModels.getModelService(this.itemsPerPage, this.currentPage).subscribe({
        next: (data: any[]) => {
          console.log("Fetched data:", data);
          this.models = [];
          data.flatMap(item => item.get_latest_models).forEach(model => {
            console.log("Model:", model)
              this.models?.push(new Model(
                model.model_id,
                model.model_name,
                model.epochs,
                model.num_frames,
                model.batch_size,
                new Date(model.creation_date),
                model.train,
                model.test,
                model.verification,
                model.shuffle_size,
                model.location_name))
              });
            },
        error: (error) => console.error('Error fetching models:', error)
      });
    }

    fetchConfigurationMap(){
      this.mapService.fetchConfigurationMap().subscribe({
        next: (data: any[]) => {
          console.log("Fetched config map:", data);
          this.configMap = [];
          data.flatMap(item => item.get_configuration_map).forEach(config => {
            console.log("Model:", config)
              this.configMap.push(new ModelConfig(
                config.config_id,
                config.config_name,
                config.epochs,
                config.num_frames,
                config.batch_size,
                config.train,
                config.test,
                config.verification,
                config.shuffle_size))
              });
            },
        error: (error) => console.error('Error fetching models:', error)
      });
    }

  mapModelConfiguration(model: Model){
    let configName = "Advanced"
    console.log("Mapping Model", model.model_name)
    for (const configuration of this.configMap) {
      if (this.findModelMapping(model, configuration)) {
        console.log("Found match:", configuration.config_name);
        configName = configuration.config_name;
        break; 
      }
    }
    return configName;
    }

  findModelMapping(model: Model, configuration: ModelConfig) {
    let doesMatch = false;
    if(model.test === configuration.test &&
              model.train === configuration.train &&
              model.epochs === configuration.epochs &&
              model.batch_size === configuration.batch_size &&
              model.num_frames === configuration.num_frames &&
              model.shuffle_size === configuration.shuffle_size &&
              model.verification === configuration.verification){
              doesMatch = true;
              }
    return doesMatch;
    } 

    // Class Functions
    organiseClasses(){
      this.categoriesService.getCategories().subscribe(categorisedClasses => {
        this.categorisedClasses = categorisedClasses[0]?.get_categorised_classes;
        if (this.categorisedClasses && this.categoryMap && this.classMap) {
          this.categorisedClassesString = this.convertToText(this.categorisedClasses, this.categoryMap, this.classMap);
          if(this.categorisedClassesString){
            this.categories = Object.keys(this.categorisedClassesString);
            this.categoriesExpanded = this.categories.map(() => false);
          }
          this.cdr.detectChanges();
        } else {
        }
      });
    }

    selectValues(category: string){
      if(this.categorisedClassesString){
        return this.categorisedClassesString[category]
      }
      else{
        return
      }
    }

    getClasses(){
      this.phase1 = false;
      this.previousButtonStatus = false;
      this.organiseClasses();
    };

    convertToText(originalJson: any, categoriesMap: Map, classesMap: Map): any {
      const remapped = Object.keys(originalJson).reduce((acc: any, key) => {
        const category = categoriesMap[key];
        const classIds = originalJson[key];
        const classTexts = classIds.map((classId: string) => classesMap[classId.toString()]);
        acc[category] = classTexts;
        return acc;
      }, {});
  
      return remapped;
    } 

    fetchCategoryMap(){
      this.mapService.fetchCategoryMap().subscribe(categoryMaps => {
        this.categoryMap = categoryMaps[0]?.get_categories_map;
        if (this.categoryMap) {
          this.cdr.detectChanges();
        } else {
          console.log('Category map not retrieved');
        }
      });
    }

  fetchClassMap(){
    this.mapService.fetchClassMap().subscribe(classMaps => {
      this.classMap = classMaps[0]?.get_class_map;
      if (this.classMap) {
        this.cdr.detectChanges();
        }
      else {
        console.log('Class map not retrieved');
      }
    });
  }

    placeholder(){}
}
