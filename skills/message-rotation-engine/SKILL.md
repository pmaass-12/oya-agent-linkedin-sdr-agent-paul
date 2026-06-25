---
name: message-rotation-engine
display_name: "Message Rotation Engine"
description: "Rotates through personalized outreach message variants (curiosity, pain-point, social proof, direct-ask) by merging prospect details into the next template in sequence."
category: sales
icon: rotate-cw
skill_type: sandbox
catalog_type: addon
tool_schema:
  name: message_rotation_engine
  description: "Selects the next message template variant in rotation, personalizes it with the prospect's details, and returns the composed message plus the new variant index for memory persistence."
  parameters:
    type: object
    properties:
      templates:
        type: array
        items:
          type: string
        description: "Ordered list of message templates. Each should contain tokens like {{first_name}}, {{company}}, {{title}}. The order defines the rotation cycle (e.g. curiosity → pain-point → social proof → direct-ask)."
      first_name:
        type: string
        description: "Prospect's first name, replaces {{first_name}} in the template."
      title:
        type: string
        description: "Prospect's job title, replaces {{title}} in the template."
      company:
        type: string
        description: "Prospect's company name, replaces {{company}} in the template."
      last_variant_index:
        type: integer
        description: "The index of the last-used template variant (from Agent Memory). Use -1 if no message has been sent yet."
        default: -1
    required: [templates, first_name, title, company, last_variant_index]
---
# Message Rotation Engine
Cycles through Paul's outreach templates in order, personalizes each with prospect tokens, and returns the ready-to-send message plus the next index to store in memory.

## Be Proactive
Call this skill whenever Paul wants to send or prepare a personalized outreach message to a prospect — it automatically picks the correct next variant and fills in the prospect's details.