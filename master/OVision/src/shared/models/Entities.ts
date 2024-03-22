    export class Target {
        constructor(
            public target_id:number, 
            public target_name: string,
            public alt_name: string,
            public creation_date: Date,
            public status_value: 'Active' | 'Complete' | 'Expiring' | 'Error' | 'New' | 'Disabled',
        ) {}
    }

    export class Person extends Target {
        public dob: Date;
        public role: string;
        public age: number;

        constructor(
            target_id:number, 
            target_name: string, 
            alt_name: string, 
            creation_date: Date, 
            status_value: 'Active' | 'Complete' | 'Expiring' | 'Error' | 'New' | 'Disabled',
            dob: Date, 
            role: string) 
            {
            super(target_id, target_name, alt_name, creation_date, status_value);
            this.dob = dob;
            this.role = role;
            this.age = this.getAge(dob);
        }

        public getAge(dob: Date): number {
            const today = new Date();
            const age = today.getFullYear() - dob.getFullYear();
            const month = today.getMonth() - dob.getMonth();
            if (month < 0 || (month === 0 && today.getDate() < dob.getDate())) {
                return age - 1;
            }
            return age;
        }

    }

    export class Location extends Target {
        constructor(
            target_id:number,
            target_name: string,
            alt_name: string,
            creation_date: Date,
            status_value: 'Active' | 'Complete' | 'Expiring' | 'Error' | 'New' | 'Disabled',
            public access: 'public' | 'private' | null)     
            {
            super(target_id,target_name, alt_name, creation_date, status_value);
        }
    }
    
    export class BaseModelConfig {
        constructor(
            public epochs: number,
            public num_frames: number,
            public batch_size: number,
            public train: number,
            public test: number,
            public verification: number,
            public shuffle_size: number
        ) {}
    }
    
    export class Model extends BaseModelConfig {
        constructor(
            public model_id: number,
            public model_name: string,
            epochs: number,
            num_frames: number,
            batch_size: number,
            public creation_date: Date,
            train: number,
            test: number,
            verification: number,
            shuffle_size: number,
            public location_name: string
        ) {
            super(epochs, num_frames, batch_size, train, test, verification, shuffle_size);
        }
    }

    export class ModelConfig extends BaseModelConfig {
        constructor(
            public config_id: number,
            public config_name: string,
            epochs: number,
            num_frames: number,
            batch_size: number,
            train: number,
            test: number,
            verification: number,
            shuffle_size: number
        ) {
            super(epochs, num_frames, batch_size, train, test, verification, shuffle_size);
        }
    }
    
    export class Task extends BaseModelConfig {
        constructor(
            public task_id: number,
            public model_name: string,
            public creation_date: Date,
            public status_value: 'queue' | 'gathering' | 'training' | 'trained' | 'failed',
            public classes: number[],
            public sources: number[],
            epochs: number,
            num_frames: number,
            batch_size: number,
            train: number,
            test: number,
            verification: number,
            shuffle_size: number
        ) {
            super(epochs, num_frames, batch_size, train, test, verification, shuffle_size);
        }
    }

export class Deployment {
    constructor(
        public deployment_id: number,
        public deployment_name: string,
        public target_id: string,
        public status_value: 'Active' | 'Complete' | 'Expiring' | 'Error' | 'New' | 'Disabled',
        public model_id: string,
        public creation_date: Date,
        public start_date: Date,
        public expiry_date: Date,
        public node_id: number,
        public device_id: number
    ){}

    get running_time(): number {
        const currentDate = new Date();
        const startDateMidnight = new Date(this.start_date);
        startDateMidnight.setHours(0, 0, 0, 0); 
        const timeDiff = currentDate.getTime() - startDateMidnight.getTime();
        const hoursDiff = timeDiff / (1000 * 3600); 
        return Math.floor(hoursDiff); 
    }
}

export class Report {
    constructor(
        public report_id: string,
        public report_name: string,
        public deployment_id: string,
        public frequency_value: number,
        public frequency_unit: string,
        public creation_date: Date,
        public last_gen: Date | null,
        public graph_id: string,
    ) {}

    public calculateNextGen(): Date {
        let baseDate = this.last_gen ? new Date(this.last_gen) : new Date(this.creation_date);

        switch (this.frequency_unit) {
            case 'day':
                baseDate.setDate(baseDate.getDate() + this.frequency_value);
                break;
            case 'week':
                baseDate.setDate(baseDate.getDate() + (this.frequency_value * 7));
                break;
            case 'month':
                baseDate.setMonth(baseDate.getMonth() + this.frequency_value);
                break;
            case 'year':
                baseDate.setFullYear(baseDate.getFullYear() + this.frequency_value);
                break;
            default:
                throw new Error('Unsupported frequency unit');
        }
        return new Date(baseDate);
    }
}
