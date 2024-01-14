export class deploymentItem {
    constructor( public targetName : string , public status : string, public runningTime: Number, public modelName: string, public startDate: Date, public endDate: Date, public Stats: string, public Settings: string ){}
}
