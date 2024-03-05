import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Model, ModelConfig } from '../../../shared/models/Entities'
import { GetMapService } from '../../passive/get-maps.service';
import { GetCategoriesService } from './get-categories.service';
@Component({
  selector: 'app-create-models',
  templateUrl: './create-models.component.html',
  styleUrls: ['./create-models.component.sass']
})
export class CreateModelsComponent {

  advancedSettings: boolean = false;
  phase1: boolean = true;
  buttonStatus: boolean = true;

  configMap: ModelConfig[] = [];
  selectedConfig: ModelConfig | null = null;
  availableConfig: ModelConfig[] = [new ModelConfig(1,'Model 1',10,10,10,10,10,10,10), new ModelConfig(2,'Model 2',10,10,10,10,10,10,10)];
  maxLength: number = 1;

  customEpochs: number = 0;
  customNumFrames: number = 0;
  customBatchSize: number = 0;
  customTrain: number = 0;
  customTest: number = 0;
  customVerification: number = 0;
  customShuffleSize: number = 0;


  constructor(private cdr: ChangeDetectorRef,
    private mapService: GetMapService,
    private categoriesService: GetCategoriesService) { }

  onConfigChange(){
    if(this.selectedConfig){
    this.customEpochs = this.selectedConfig.epochs;
    this.customNumFrames = this.selectedConfig.num_frames;
    this.customBatchSize = this.selectedConfig.batch_size;
    this.customTrain = this.selectedConfig.train;
    this.customTest = this.selectedConfig.test;
    this.customVerification = this.selectedConfig.verification;
    this.customShuffleSize = this.selectedConfig.shuffle_size;
  };
  this.buttonStatus = false;
};

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
  };

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
};

updateSelection(){
  if (this.selectedConfig) {
    this.selectedConfig = null;
  }
    this.selectedConfig = new ModelConfig(0,
                          'Custom',
                          this.customEpochs,
                          this.customNumFrames,
                          this.customBatchSize,
                          this.customTrain,
                          this.customTest,
                          this.customVerification,
                          this.customShuffleSize);
  this.buttonStatus = false;
};

getClasses(){
  this.phase1 = false;
  this.advancedSettings = false;
};
}
