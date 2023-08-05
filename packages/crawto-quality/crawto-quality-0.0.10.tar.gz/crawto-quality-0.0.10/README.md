# Crawto-Quality
  A Collection of Tools for improving code quality

## Crawto-Doc
A command-line-tool to add numpy style docstrings to your python projects.  
From reading just your code, its a docstring with a description, parameters, and and attributes & examples where applicable.  
While it cannot totally complete your documentation, Crawto-Doc can fill in as
much information you give it. Using mypy will fill in some missing pieces.
### Why
Because documentation is a oft boring or an after-thought. 
Many programs exist to turn documentation into websites or otherwise shareable
text.  The CrawtoDoc package exists to turn code into documentation.  
### From  

    class DummyClassifier(MultiOutputMixin, ClassifierMixin, BaseEstimator):
        @_deprecate_positional_args
        def __init__(self, *, strategy="warn", random_state=None, constant=None):  
            self.strategy = strategy
            self.random_state = random_state
            self.constant = constant

### To  
    class DummyClassifier(MultiOutputMixin, ClassifierMixin, BaseEstimator):  
        """<#TODO Description>

        Parameters
        ----------
        strategy : <#TODO type definition>, default=warn
            <#TODO Description>

        random_state : <#TODO type definition>, default=None
            <#TODO Description>

        constant : <#TODO type definition>, default=None
            <#TODO Description>

        Attributes
        ----------
        sparse_output_ : <#TODO type definition>
            <#TODO Attribute Description>

        n_outputs_ : <#TODO type definition>
            <#TODO Attribute Description>

        n_features_in_ : <#TODO type definition>
            <#TODO Attribute Description>

        outputs_2d_ : <#TODO type definition>
            <#TODO Attribute Description>

        Examples
        --------
        >>> from crawto-quality import crawto_doc
        >>> example = DummyClassifier(strategy='warn', random_state=None, constant=None)
        >>> example.fit(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
        <#TODO Method Return Value>
        >>> example.predict(X=<#TODO Example Value>)
        <#TODO Method Return Value>
        >>> example.predict_proba(X=<#TODO Example Value>)
        <#TODO Method Return Value>
        >>> example.predict_log_proba(X=<#TODO Example Value>)
        <#TODO Method Return Value>
        >>> example.score(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
        <#TODO Method Return Value>
        """
