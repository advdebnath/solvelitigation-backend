import mongoose, { Schema } from "mongoose";

export interface ILegalOntology {

  section: string;

  act: string;

  category: string;

  contexts: string[];

  confidence: number;

  reviewed: boolean;

  createdAt?: Date;

  updatedAt?: Date;
}

const LegalOntologySchema =
new Schema<ILegalOntology>(

  {

    section: {

      type: String,

      required: true,

      index: true
    },

    act: {

      type: String,

      required: true,

      index: true
    },

    category: {

      type: String,

      required: true,

      index: true
    },

    contexts: {

      type: [String],

      default: []
    },

    confidence: {

      type: Number,

      default: 50
    },

    reviewed: {

      type: Boolean,

      default: false
    }
  },

  {

    timestamps: true
  }
);

// ============================================
// 🔥 UNIQUE ONTOLOGY
// ============================================

LegalOntologySchema.index(

  {

    section: 1,

    act: 1
  },

  {

    unique: true
  }
);

const LegalOntology =

  mongoose.models.LegalOntology ||

  mongoose.model<ILegalOntology>(

    "LegalOntology",

    LegalOntologySchema
  );

export default LegalOntology;
