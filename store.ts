import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type PackageType = 'corporate' | 'enterprise' | 'ngo' | 'upgrade';

export interface Package {
  id: string;
  name: string;
  price: number;
  type: PackageType;
  features: string[];
}

export interface User {
  email: string;
  role: 'client' | 'admin';
}

export interface Address {
  state: string;
  lga: string;
  city: string;
  houseNumber: string;
  streetName: string;
}

export interface EnterpriseDetails {
  proposedNames: string[]; // Business Name 1, Business Name 2
  personalDetails: {
    surname: string;
    firstName: string;
    otherName: string;
    dob: string;
    gender: string;
    phone: string;
    email: string;
    nin: string;
  };
  homeAddress: Address;
  businessAddress: Address;
  natureOfBusiness: string;
  documents: {
    ninSlipUrl?: string;
    passportPhotoUrl?: string;
    signatureUrl?: string;
  };
}

export interface DirectorShareholder {
  id: string;
  surname: string;
  firstName: string;
  otherName: string;
  dob: string;
  gender: string;
  nationality: string;
  phone: string;
  email: string;
  address: Address;
  idType: string;
  idNumber: string;
  shares?: number; // percentage of equity share (used for shareholders)
  idCardUrl?: string;
  signatureUrl?: string;
  passportPhotoUrl?: string;
}

export interface CompanyDetails {
  proposedNames: string[]; // Company Name 1, Company Name 2
  objectsOfMemorandum: string[]; // list of objects
  directors: DirectorShareholder[];
  shareholders: DirectorShareholder[];
  shareCapitalBreakdown: {
    totalShares: number;
    nominalValue: number;
    numShareholders: number;
  };
  witness: {
    surname: string;
    firstName: string;
    otherName: string;
    phone: string;
    email: string;
    address: Address;
  };
}

export interface Trustee {
  id: string;
  fullName: string;
  role: string; // Chairman, Secretary, Treasurer, Member
  nin: string;
  dob: string;
  gender: string;
  occupation: string;
  address: string;
  passportPhotoUrl?: string;
  ninUploadUrl?: string;
}

export interface NgoDetails {
  representative: {
    surname: string;
    firstName: string;
    otherName: string;
    dob: string;
    gender: string;
    nationality: string;
    phone: string;
    email: string;
    occupation: string;
  };
  proposedNames: string[]; // Proposed Name 1, Proposed Name 2, Proposed Name 3
  mission: string;
  officeAddress: {
    houseNumber: string;
    streetName: string;
    city: string;
    lga: string;
    state: string;
  };
  utilityBillUrl?: string;
  trustees: Trustee[];
  aimsAndObjectives: string[];
}

export interface IntakeData {
  idScanCompleted: boolean;
  scannedIdUrl: string | null;
  scannedIdName: string | null;
  enterpriseDetails: EnterpriseDetails;
  companyDetails: CompanyDetails;
  ngoDetails: NgoDetails;
}

export interface ClientProfile {
  id: string;
  email: string;
  package: Package;
  status: 'payment_pending' | 'intake' | 'review' | 'filed' | 'completed';
  intakeData: IntakeData;
  actionNeeded: string | null;
  submittedAt?: string;
  progress: number;
  paymentStatus?: "pending" | "partially_paid" | "fully_paid";
  deliverables?: { id: string; name: string; url: string; date: string }[];
}

export interface AppState {
  user: User | null;
  setUser: (user: User | null) => void;
  selectedPackage: Package | null;
  setSelectedPackage: (pkg: Package | null) => void;
  intakeData: IntakeData;
  updateIntakeData: (data: Partial<IntakeData>) => void;
  resetIntakeData: () => void;
  applicationStatus: 'payment_pending' | 'intake' | 'review' | 'filed' | 'completed';
  setApplicationStatus: (status: AppState['applicationStatus']) => void;
  actionNeeded: string | null;
  setActionNeeded: (action: string | null) => void;
  
  // Admin mock state
  clients: ClientProfile[];
  updateClient: (id: string, updates: Partial<ClientProfile>) => void;
  addClient: (client: ClientProfile) => void;
}

const initialAddress: Address = {
  state: '',
  lga: '',
  city: '',
  houseNumber: '',
  streetName: '',
};

export const initialIntakeData: IntakeData = {
  idScanCompleted: false,
  scannedIdUrl: null,
  scannedIdName: null,
  enterpriseDetails: {
    proposedNames: ['', ''],
    personalDetails: {
      surname: '',
      firstName: '',
      otherName: '',
      dob: '',
      gender: '',
      phone: '',
      email: '',
      nin: '',
    },
    homeAddress: { ...initialAddress },
    businessAddress: { ...initialAddress },
    natureOfBusiness: '',
    documents: {},
  },
  companyDetails: {
    proposedNames: ['', ''],
    objectsOfMemorandum: ['1. Sale and supply of general merchandise'],
    directors: [],
    shareholders: [],
    shareCapitalBreakdown: {
      totalShares: 1000000,
      nominalValue: 1,
      numShareholders: 1,
    },
    witness: {
      surname: '',
      firstName: '',
      otherName: '',
      phone: '',
      email: '',
      address: { ...initialAddress },
    },
  },
  ngoDetails: {
    representative: {
      surname: '',
      firstName: '',
      otherName: '',
      dob: '',
      gender: '',
      nationality: 'Nigerian',
      phone: '',
      email: '',
      occupation: '',
    },
    proposedNames: ['', '', ''],
    mission: '',
    officeAddress: {
      houseNumber: '',
      streetName: '',
      city: '',
      lga: '',
      state: '',
    },
    utilityBillUrl: undefined,
    trustees: [],
    aimsAndObjectives: ['1. To promote social and economic welfare of the community.'],
  },
};

// Mock initial admin profiles

const sanitizeString = (str: string) => {
  return str.replace(/<[^>]*>?/gm, '');
};

const deepSanitize = (obj: any): any => {
  if (typeof obj === 'string') {
    return sanitizeString(obj);
  }
  if (Array.isArray(obj)) {
    return obj.map(deepSanitize);
  }
  if (typeof obj === 'object' && obj !== null) {
    const newObj: any = {};
    for (const key in obj) {
      newObj[key] = deepSanitize(obj[key]);
    }
    return newObj;
  }
  return obj;
};

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
      selectedPackage: null,
      setSelectedPackage: (pkg) => set({ selectedPackage: pkg }),
      intakeData: initialIntakeData,
      updateIntakeData: (data) => set((state) => ({ intakeData: { ...state.intakeData, ...deepSanitize(data) } })),
      resetIntakeData: () => set({ intakeData: initialIntakeData }),
      applicationStatus: 'payment_pending',
      setApplicationStatus: (status) => set({ applicationStatus: status }),
      actionNeeded: null,
      setActionNeeded: (action) => set({ actionNeeded: action }),
      
      clients: [],
      updateClient: (id, updates) => set((state) => ({
        clients: state.clients.map(c => c.id === id ? { ...c, ...updates } : c)
      })),
      addClient: (client) => set((state) => ({
        clients: [client, ...state.clients]
      }))
    }),
    {
      name: 'budutech-flow-storage', // localstorage key
      partialize: (state) => ({
        user: state.user,
        selectedPackage: state.selectedPackage,
        intakeData: state.intakeData,
        applicationStatus: state.applicationStatus,
        actionNeeded: state.actionNeeded,
      }),
    }
  )
);
