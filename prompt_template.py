# Configurable prompt template for medical documentation review

SYSTEM_PROMPT = """
You are an expert medical documentation auditor with extensive knowledge of medical protocols, 
prescribing practices, and documentation requirements. Review the provided medical documentation 
and answer the following questions with only 'Yes', 'No', 'Partial', or 'N/A' where appropriate, 
and provide brief explanations where requested.
"""

QUESTION_TEMPLATE = """
Based on the following medical documentation, please answer these questions:

{medical_documentation}

1. Was a mental status exam performed? 
2. Was the patient assessed for Suicidal/Homicidal ideation?
3. What is the diagnosis?
4. Is the diagnosis supported by the exam, assessment, and follow-up plan and is it documented?
5. Were the appropriate doses of medication prescribed for each diagnosis?
6. Document dose and quantity of medication prescribed:
7. Any additional comments: 
8. If controlled substances were prescribed, was this done appropriately?
9. Have proper drug screening and wean protocols been followed?
10. Were vital signs assessed?
"""

def generate_prompt(medical_documentation):
    """
    Generate a prompt for the OpenAI API using the medical documentation.
    
    Args:
        medical_documentation (str): The medical documentation text.
        
    Returns:
        str: The formatted prompt.
    """
    return QUESTION_TEMPLATE.format(medical_documentation=medical_documentation)

def customize_prompt(template=QUESTION_TEMPLATE):
    """
    Allows customization of the prompt template.
    
    Args:
        template (str, optional): New template to use. Defaults to QUESTION_TEMPLATE.
        
    Returns:
        str: The updated template.
    """
    return template 